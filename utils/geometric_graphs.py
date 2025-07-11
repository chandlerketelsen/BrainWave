import os
import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data, DataLoader
from scipy.spatial import distance_matrix

distance_threshold = 75
labels_folder = ""
batch_size = 32

def process_csv(csv_path, dist_threshold):
    df = pd.read_csv(csv_path)
    df = df.sort_values(by="node_id")

    node_features = torch.tensor(df[["is_handicapped"]].values, dtype=torch.float)
    labels = torch.tensor(df["is_occupied"].values, dtype=torch.long)

    coords = df[["x_pixel", "y_pixel"]].to_numpy()
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

def build_graph_dataset(root_dir):
    data_list = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(subdir, file)
                data = process_csv(csv_path)
                data_list.append(data)
    return data_list

data_list = build_graph_dataset(labels_folder)
loader = DataLoader(data_list, batch_size=batch_size, shuffle=True)