import os
import pandas as pd
import numpy as np
from torch_geometric_temporal import temporal_signal_split
from torch_geometric_temporal.signal import DynamicGraphTemporalSignal
from scipy.spatial import distance_matrix

def compute_distance(x, y, x_center=967, y_center=936):
    return np.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)

def process_csv_file(path, x_center=967, y_center=936):
    df = pd.read_csv(path)

    df['store_distance'] = compute_distance(df['x_pixel'], df['y_pixel'], x_center, y_center)
    df.to_csv(path, index=False)

def process_all_partitions(root_dir=""):
    for partition in os.listdir(root_dir):
        partition_path = os.path.join(root_dir, partition)
        labels_dir = os.path.join(partition_path, "labels")

        if not os.path.isdir(labels_dir):
            continue

        for file in os.listdir(labels_dir):
            if file.endswith(".csv"):
                csv_path = os.path.join(labels_dir, file)
                process_csv_file(csv_path)

def process_csv(csv_path):
    df = pd.read_csv(csv_path).sort_values(by="node_id")

    min_dist = df["store_distance"].min()
    max_dist = df["store_distance"].max()
    df["store_distance_norm"] = (df["store_distance"] - min_dist) / (max_dist - min_dist + 1e-8)

    features = df[["is_handicapped", "store_distance_norm"]].to_numpy().astype(np.float32)
    labels = df["is_occupied"].to_numpy().astype(np.float32)
    coords = df[["x_pixel", "y_pixel"]].to_numpy()

    return features, labels, coords

def build_dynamic_dataset(root_dir, dist_threshold=75):
    csv_paths = sorted([
        os.path.join(subdir, file)
        for subdir, _, files in os.walk(root_dir)
        for file in files if file.endswith(".csv") and file != "nodes.csv"
    ])

    features_list = []
    targets_list = []
    edge_indices_list = []
    edge_weights_list = []

    sigma = dist_threshold / 2

    for path in csv_paths:
        x, y, coords = process_csv(path)

        dist_mat = distance_matrix(coords, coords)
        
        edge_list = []
        edge_weights = []

        for i in range(len(coords)):
            for j in range(len(coords)):
                if i != j and dist_mat[i, j] <= dist_threshold:
                    edge_list.append([i, j])
                    weight = np.exp(- (dist_mat[i, j] ** 2) / (2 * sigma ** 2))
                    edge_weights.append(weight)

        edge_index = np.array(edge_list).T.astype(np.int64)
        edge_weight = np.array(edge_weights, dtype=np.float32)

        features_list.append(x)
        targets_list.append(y)
        edge_indices_list.append(edge_index)
        edge_weights_list.append(edge_weight)

    dataset = DynamicGraphTemporalSignal(
        edge_indices=edge_indices_list,
        edge_weights=edge_weights_list,
        features=features_list,
        targets=targets_list,
    )

    train_dataset, val_dataset = temporal_signal_split(dataset, train_ratio=0.8)
    val_dataset, test_dataset = temporal_signal_split(val_dataset, train_ratio=0.5)
    return train_dataset, val_dataset, test_dataset