import cv2
import pandas as pd
import os
import numpy as np

image_folder = ""
output_folder = ""
nodes_csv = ""
window_size = 8
diff_threshold = 25
os.makedirs(output_folder, exist_ok=True)

nodes = pd.read_csv(nodes_csv)
positions = nodes[['x_pixel', 'y_pixel']].values.astype(int)
node_ids = nodes['node_id'].values
is_handicapped = nodes['is_handicapped'].values
prev_occupancy = nodes['is_occupied'].tolist()

image_files = sorted(f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.png')))

first_img_path = os.path.join(image_folder, image_files[0])
first_frame = cv2.imread(first_img_path)
prev_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

for idx in range(1, len(image_files)):
    img_file = image_files[idx]
    img_path = os.path.join(image_folder, img_file)
    name = os.path.splitext(img_file)[0]
    output_path = os.path.join(output_folder, f"{name}_labels.csv")

    frame = cv2.imread(img_path)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    occupancy = []

    for i, (x, y) in enumerate(positions):
        x1, x2 = max(0, x - window_size), min(frame.shape[1], x + window_size)
        y1, y2 = max(0, y - window_size), min(frame.shape[0], y + window_size)

        current_patch = frame_gray[y1:y2, x1:x2]
        prev_patch = prev_frame[y1:y2, x1:x2]

        current_patch = cv2.GaussianBlur(current_patch, (3, 3), 0)
        prev_patch = cv2.GaussianBlur(prev_patch, (3, 3), 0)

        diff = np.mean(np.abs(current_patch.astype(np.int16) - prev_patch.astype(np.int16)))

        if diff > diff_threshold:
            occ = 1 - prev_occupancy[i]
        else:
            occ = prev_occupancy[i]

        occupancy.append(occ)

    print(f"Frame: {img_file} — Occupied spots: {sum(occupancy)}/{len(occupancy)}")

    df = pd.DataFrame({
        "node_id": node_ids,
        "x_pixel": positions[:, 0],
        "y_pixel": positions[:, 1],
        "is_handicapped": is_handicapped,
        "is_occupied": occupancy
    })
    df.to_csv(output_path, index=False)

    prev_frame = frame_gray
    prev_occupancy = occupancy.copy()