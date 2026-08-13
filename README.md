# 🚗 YOLOv8 Vehicle Speed Detection

Estimates vehicle speed from video using **YOLOv8** for detection and **Norfair** for tracking. Vehicles are tracked as they cross two reference lines; speed is calculated from the time taken to travel the known real-world distance between them.

## Features
- Real-time vehicle/object detection (YOLOv8)
- Multi-object tracking with persistent IDs (Norfair)
- Line-crossing based speed estimation (km/h)
- On-screen line & speed overlay + console logging
- Click-to-get-coordinates tool for easy line calibration

## Setup

```bash
pip install opencv-python ultralytics norfair numpy
```

YOLOv8 weights (`yolov8l.pt`) auto-download on first run if not present.

## Configuration

Edit these in the script for your video:

| Variable | What it does |
|---|---|
| `red_line_1_y`, `red_line_2_y` | Y-coordinates of the two reference lines |
| `real_distance_meters` | Real-world distance (m) between the two lines |
| `DISPLAY_WIDTH` | Resize width for the video window |
| `cap = cv2.VideoCapture(...)` | `0` for webcam, or a file path |
| `device="cpu"` / `"cuda"` | Use `"cuda"` only if you have GPU + CUDA set up |

**To calibrate lines:** run the script, click on the road in the video window, read the printed `x, y` coordinates from the terminal, and set `red_line_1_y` / `red_line_2_y` accordingly.

**To estimate `real_distance_meters`:** use known references in frame (car length ≈ 4.5m, lane width ≈ 3–3.5m) to approximate the distance between your two lines.

## Usage

```bash
python Vehicle_Speed_Detection.py
```

Press **`q`** to quit.

## Limitations
- Assumes a fairly straight-on camera angle (no perspective correction)
- CPU inference is slow (~1–3 FPS with `yolov8l.pt`) — try `yolov8n.pt`/`yolov8s.pt` for speed
- Built for one-way traffic crossing the lines in a single direction

## Future Improvements
- Perspective correction for accurate distance mapping
- Multi-lane support, bidirectional tracking
- CSV/data logging, speed smoothing, simple GUI
