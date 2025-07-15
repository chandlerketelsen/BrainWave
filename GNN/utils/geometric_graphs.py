import os
import pandas as pd
import numpy as np
from torch_geometric_temporal import temporal_signal_split
from torch_geometric_temporal.signal import DynamicGraphTemporalSignal
from scipy.spatial import distance_matrix

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
    return train_dataset, val_dataset

distance_threshold = 75
train_dataset, val_dataset = build_dynamic_dataset("Data", dist_threshold=distance_threshold)