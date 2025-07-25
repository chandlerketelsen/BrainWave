import os
import pandas as pd
import numpy as np
from torch_geometric_temporal import temporal_signal_split
from torch_geometric_temporal.signal import DynamicGraphTemporalSignalBatch
from scipy.spatial import distance_matrix
from datetime import datetime, timedelta
import math

def compute_distance(x, y, x_center, y_center):
    return np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)

def extract_base_time_from_folder(folder_name):
    try:
        parts = folder_name.split("_")
        timestamp_str = parts[1]
        dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
        return dt
    except Exception as e:
        print(f"Error parsing base time from folder {folder_name}: {e}")
        return None

def extract_frame_number(file_name):
    try:
        parts = file_name.split("_")
        frame_str = parts[2]  # e.g., 0001
        return int(frame_str)
    except Exception as e:
        print(f"Error parsing frame number from file {file_name}: {e}")
        return 0

def compute_time_features_from_datetime(dt):
    time_of_day = dt.hour + dt.minute / 60 + dt.second / 3600
    normalized_time = time_of_day / 24.0
    sin_time = math.sin(2 * math.pi * normalized_time)
    cos_time = math.cos(2 * math.pi * normalized_time)
    return sin_time, cos_time

def process_csv_file(csv_path, folder_name, file_name, x_center=967, y_center=936):
    df = pd.read_csv(csv_path)

    df['store_distance'] = compute_distance(df['x_pixel'], df['y_pixel'], x_center, y_center)

    base_time = extract_base_time_from_folder(folder_name)
    frame_number = extract_frame_number(file_name)

    if base_time is None:
        sin_time, cos_time = 0.0, 0.0
    else:
        frame_time = base_time + timedelta(seconds=frame_number)
        sin_time, cos_time = compute_time_features_from_datetime(frame_time)

    df['time_sin'] = sin_time
    df['time_cos'] = cos_time

    df.to_csv(csv_path, index=False)

def process_all_partitions(root_dir):
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder)
        labels_dir = os.path.join(folder_path, "labels")

        if not os.path.isdir(labels_dir):
            continue

        for file in os.listdir(labels_dir):
            if file.endswith(".csv"):
                csv_path = os.path.join(labels_dir, file)
                process_csv_file(csv_path, folder, file)

def process_csv(csv_path):
    df = pd.read_csv(csv_path).sort_values(by="node_id")

    min_dist = df["store_distance"].min()
    max_dist = df["store_distance"].max()
    df["store_distance_norm"] = (df["store_distance"] - min_dist) / (max_dist - min_dist + 1e-8)

    features = df[["is_handicapped", "store_distance_norm", "time_sin", "time_cos"]].to_numpy().astype(np.float32)
    labels = df["is_occupied"].to_numpy().astype(np.float32)
    coords = df[["x_pixel", "y_pixel"]].to_numpy()

    return features, labels, coords

def build_dynamic_dataset(root_dir, batch_size=32, dist_threshold=75):
    csv_paths = sorted([
        os.path.join(subdir, file)
        for subdir, _, files in os.walk(root_dir)
        for file in files if file.endswith(".csv") and file != "nodes.csv"
    ])

    def build_graph(path):
        x, y, coords = process_csv(path)

        dist_mat = distance_matrix(coords, coords)
        edge_list = []
        edge_weights = []

        sigma = dist_threshold / 2

        for i in range(len(coords)):
            for j in range(len(coords)):
                if i != j and dist_mat[i, j] <= dist_threshold:
                    edge_list.append([i, j])
                    weight = np.exp(- (dist_mat[i, j] ** 2) / (2 * sigma ** 2))
                    edge_weights.append(weight)

        edge_index = np.array(edge_list).T.astype(np.int64)
        edge_weight = np.array(edge_weights, dtype=np.float32)
        return x, y, edge_index, edge_weight

    x_all, y_all, ei_all, ew_all = [], [], [], []
    for path in csv_paths:
        x, y, ei, ew = build_graph(path)
        x_all.append(x)
        y_all.append(y)
        ei_all.append(ei)
        ew_all.append(ew)

    batched_x, batched_y, batched_ei, batched_ew, batched_batch = [], [], [], [], []

    for i in range(0, len(x_all), batch_size):
        x_batch = []
        y_batch = []
        ei_batch = []
        ew_batch = []
        batch_idx = []

        node_offset = 0
        for j, (x, y, ei, ew) in enumerate(zip(x_all[i:i + batch_size], y_all[i:i + batch_size],
                                               ei_all[i:i + batch_size], ew_all[i:i + batch_size])):
            x_batch.append(x)
            y_batch.append(y)
            ei_batch.append(ei + node_offset)
            ew_batch.append(ew)
            batch_idx.append(np.full((x.shape[0],), j, dtype=np.int64))
            node_offset += x.shape[0]

        batched_x.append(np.vstack(x_batch))
        batched_y.append(np.hstack(y_batch))
        batched_ei.append(np.hstack(ei_batch))
        batched_ew.append(np.hstack(ew_batch))
        batched_batch.append(np.hstack(batch_idx))

    dataset = DynamicGraphTemporalSignalBatch(
        edge_indices=batched_ei,
        edge_weights=batched_ew,
        features=batched_x,
        targets=batched_y,
        batches=batched_batch,
    )

    train_dataset, val_dataset = temporal_signal_split(dataset, train_ratio=0.8)
    val_dataset, test_dataset = temporal_signal_split(val_dataset, train_ratio=0.5)

    return train_dataset, val_dataset, test_dataset