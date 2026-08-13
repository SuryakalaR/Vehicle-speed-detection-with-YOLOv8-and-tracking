import cv2
import time
import numpy as np
from norfair import Tracker, Detection
from ultralytics import YOLO


model = YOLO("yolov8l.pt")


cap = cv2.VideoCapture("traffic_video.mp4")#or give video path


fps = cap.get(cv2.CAP_PROP_FPS)  

tracker = Tracker(distance_function="euclidean", distance_threshold=30)


real_distance_meters = 10


red_line_1_y = 260  
red_line_2_y = 450  


vehicle_frames = {} 
vehicle_speeds = {}  

frame_count = 0  

# --- ADDED: resize target width (adjust if still too big/small) ---
DISPLAY_WIDTH = 960

def show_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked at: x={x}, y={y}")

cv2.namedWindow("Speed Detection", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Speed Detection", show_coordinates)
# ---------------------------------------------------------------------

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1 

    # --- ADDED: resize the frame down before processing/display ---
    h, w = frame.shape[:2]
    scale = DISPLAY_WIDTH / w
    frame = cv2.resize(frame, (DISPLAY_WIDTH, int(h * scale)))
    # ----------------------------------------------------------------

    results = model.predict(frame, device="cpu", conf=0.5)
    detections = []

    for box in results[0].boxes.data:
        x1, y1, x2, y2, conf, cls = box.tolist()
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2
        detections.append(Detection(points=np.array([[x_center, y_center]])))

    tracked_objects = tracker.update(detections=detections)

    for obj in tracked_objects:
        x, y = obj.estimate[0] 
        obj_id = obj.id

       
        if red_line_1_y - 10 <= y <= red_line_1_y + 10 and obj_id not in vehicle_frames:
            vehicle_frames[obj_id] = frame_count
            print(f"Vehicle {obj_id} crossed first red line at frame {frame_count}")

        
        elif red_line_2_y - 10 <= y <= red_line_2_y + 10 and obj_id in vehicle_frames:
            frame_diff = frame_count - vehicle_frames[obj_id]
            time_diff = frame_diff / fps  

            speed = (real_distance_meters / time_diff) * 3.6 
            vehicle_speeds[obj_id] = speed

            print(f"Vehicle {obj_id} speed: {speed:.2f} km/h")

            del vehicle_frames[obj_id] 

       
        if obj_id in vehicle_speeds:
            speed = vehicle_speeds[obj_id]
            text = f"Speed: {speed:.2f} km/h"
            cv2.putText(frame, text, (int(x) - 10, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

   
    cv2.line(frame, (0, red_line_1_y), (frame.shape[1], red_line_1_y), (0, 0, 255), 2)
    cv2.line(frame, (0, red_line_2_y), (frame.shape[1], red_line_2_y), (0, 0, 255), 2)


    cv2.imshow("Speed Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()