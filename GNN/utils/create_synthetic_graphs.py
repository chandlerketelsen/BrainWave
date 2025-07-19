import os
import pandas as pd
import numpy as np
import shutil
from datetime import datetime, timedelta
import re
from tqdm import tqdm
import math

data_root = ''
output_dir = ''

store_center = (967, 936)
x_center, y_center = store_center

def extract_timestamp_from_filename(filename):
    match = re.match(r'DJI_(\d{14})_', filename)
    if match:
        return datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
    return None

def get_all_graph_paths(data_root):
    graph_paths = []
    for root, dirs, files in os.walk(data_root):
        for file in files:
            if file.endswith('.csv') and file.startswith('DJI_'):
                full_path = os.path.join(root, file)
                timestamp = extract_timestamp_from_filename(file)
                if timestamp:
                    graph_paths.append((timestamp, full_path))
    graph_paths.sort(key=lambda x: x[0])
    return graph_paths

def compute_time_features(dt):
    time_of_day = dt.hour + dt.minute / 60 + dt.second / 3600
    normalized_time = time_of_day / 24.0
    sin_time = math.sin(2 * math.pi * normalized_time)
    cos_time = math.cos(2 * math.pi * normalized_time)
    return sin_time, cos_time

def interpolate_graphs(g1_df, g2_df, alpha):
    interp_df = g1_df.copy()
    for col in g1_df.columns:
        if col == 'is_occupied':
            interp_df[col] = (1 - alpha) * g1_df[col] + alpha * g2_df[col]
            interp_df[col] = interp_df[col].round().astype(int)
        elif np.issubdtype(g1_df[col].dtype, np.number):
            interp_df[col] = (1 - alpha) * g1_df[col] + alpha * g2_df[col]
    return interp_df

def generate_interpolated_graphs(graph_paths, output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for i in tqdm(range(len(graph_paths) - 1)):
        t1, path1 = graph_paths[i]
        t2, path2 = graph_paths[i + 1]
        delta = int((t2 - t1).total_seconds())

        g1 = pd.read_csv(path1)
        g2 = pd.read_csv(path2)

        sin_time, cos_time = compute_time_features(t1)
        g1['time_sin'] = sin_time
        g1['time_cos'] = cos_time
        original_filename = os.path.basename(path1)
        g1.to_csv(os.path.join(output_dir, original_filename), index=False)

        for s in range(1, delta):
            intermediate_time = t1 + timedelta(seconds=s)
            alpha = s / delta
            interp_df = interpolate_graphs(g1, g2, alpha)

            sin_time, cos_time = compute_time_features(intermediate_time)
            interp_df['time_sin'] = sin_time
            interp_df['time_cos'] = cos_time

            interp_filename = f"DJI_{intermediate_time.strftime('%Y%m%d%H%M%S')}_interp_{i}_{s}.csv"
            interp_df.to_csv(os.path.join(output_dir, interp_filename), index=False)

    t_last, path_last = graph_paths[-1]
    g_last = pd.read_csv(path_last)
    sin_time, cos_time = compute_time_features(t_last)
    g_last['time_sin'] = sin_time
    g_last['time_cos'] = cos_time
    g_last.to_csv(os.path.join(output_dir, os.path.basename(path_last)), index=False)