import cv2
import pandas as pd

image_path = ""
mask_path = ""
nodes_csv = ""
output_csv = ""
distance_threshold = 8

image = cv2.imread(image_path)
mask = cv2.imread(mask_path)

nodes = pd.read_csv(nodes_csv)
positions = nodes[['x_pixel', 'y_pixel']].values.astype(int)
node_ids = nodes['node_id'].values
is_handicapped = nodes['is_handicapped'].values
occupancy = nodes['is_occupied'].values.tolist()

annotated = cv2.addWeighted(image, 1.0, mask, 1.0, 0)
display = annotated.copy()
window_name = "Manual Occupancy Annotation"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def draw_overlay():
    global display
    display = annotated.copy()
    for i, (x, y) in enumerate(positions):
        color = (0, 255, 0) if occupancy[i] == 0 else (0, 0, 255)
        cv2.circle(display, (x, y), 6, color, -1)
    cv2.imshow(window_name, display)

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (nx, ny) in enumerate(positions):
            if ((x - nx) ** 2 + (y - ny) ** 2) ** 0.5 < distance_threshold:
                occupancy[i] = 1 - occupancy[i]
                print(f"Toggled node {node_ids[i]} → {occupancy[i]}")
                draw_overlay()
                break

cv2.setMouseCallback(window_name, click_event)
draw_overlay()

while True:
    key = cv2.waitKey(0) & 0xFF
    if key == ord('s'):
        df = pd.DataFrame({
            "node_id": node_ids,
            "x_pixel": positions[:, 0],
            "y_pixel": positions[:, 1],
            "is_handicapped": is_handicapped,
            "is_occupied": occupancy
        })
        df.to_csv(output_csv, index=False)
        break
    elif key == 27:
        break

cv2.destroyAllWindows()