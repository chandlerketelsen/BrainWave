import os
import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data
from scipy.spatial import distance_matrix

def process_csv(csv_path):
    df = pd.read_csv(csv_path)
    df = df.sort_values(by="node_id")

    node_features = df[["is_handicapped"]].values
    labels = df["is_occupied"].values
    coords = df[["x_pixel", "y_pixel"]].to_numpy()

    return node_features, labels, coords

def process_sequence(csv_paths, dist_threshold=75):
    feature_seq = []

    for path in csv_paths:
        features, labels_step, coords = process_csv(path)
        feature_seq.append(features)
        labels = labels_step

    feature_seq = np.stack(feature_seq, axis=-1)
    node_features = torch.tensor(feature_seq, dtype=torch.float)
    labels = torch.tensor(labels, dtype=torch.long)

    dist_mat = distance_matrix(coords, coords)

    edge_list = [
        [i, j]
        for i in range(len(coords))
        for j in range(len(coords))
        if i != j and dist_mat[i, j] <= dist_threshold
    ]

    edge_index = torch.tensor(edge_list, dtype=torch.long).T
    edge_index = torch.cat([edge_index, edge_index.flip(0)], dim=1)

    return Data(x=node_features, edge_index=edge_index, y=labels)

def build_graph_dataset(root_dir, distance_threshold=75, sequence_length=16):
    data_list = []
    csv_paths = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_paths.append(os.path.join(subdir, file))

    csv_paths = sorted(csv_paths)

    for i in range(len(csv_paths) - sequence_length):
        seq_paths = csv_paths[i:i + sequence_length]
        data = process_sequence(seq_paths, distance_threshold)
        data_list.append(data)

    return data_list