import cv2
import pandas as pd
import numpy as np

image_path = ""
output_csv = ""
output_mask = ""

coords = []
handicapped_flag = False
occupied_flag = False
node_id = 0

img = cv2.imread(image_path)
mask = np.zeros_like(img)

def click_event(event, x, y, flags, param):
    global node_id, handicapped_flag, occupied_flag

    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((node_id, x, y, int(handicapped_flag), int(occupied_flag)))

        if handicapped_flag and occupied_flag:
            color = (255, 255, 0)
        elif handicapped_flag:
            color = (255, 0, 0)
        elif occupied_flag:
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)

        cv2.circle(img, (x, y), 5, color, -1)
        cv2.putText(img, str(node_id), (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        mask_color = (255, 0, 0) if handicapped_flag else (0, 255, 0)
        cv2.circle(mask, (x, y), 5, mask_color, -1)
        cv2.putText(mask, str(node_id), (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        node_id += 1
        handicapped_flag = False
        occupied_flag = False

        cv2.imshow("Click Parking Spots", img)

cv2.namedWindow("Click Parking Spots")
cv2.setMouseCallback("Click Parking Spots", click_event)
cv2.imshow("Click Parking Spots", img)

while True:
    key = cv2.waitKey(0) & 0xFF

    if key == ord('h'):
        handicapped_flag = True
    elif key == ord('o'):
        occupied_flag = True
    elif key == ord('s'):
        break
    elif key == ord('q'):
        coords = []
        break

cv2.destroyAllWindows()

if coords:
    df = pd.DataFrame(coords, columns=["node_id", "x_pixel", "y_pixel", "is_handicapped", "is_occupied"])
    df.to_csv(output_csv, index=False)
    cv2.imwrite(output_mask, mask)