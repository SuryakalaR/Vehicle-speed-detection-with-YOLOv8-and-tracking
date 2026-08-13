# Vehicle Speed Detection using YOLOv8 + Norfair

This is a small project I built to estimate how fast vehicles are moving in a video, using YOLOv8 for detecting cars/buses/trucks and Norfair to track them across frames. The idea is simple — a vehicle crosses two lines drawn on the video, and based on how long it takes to go from one line to the other (plus the real-world distance between them), we calculate its speed in km/h.

It's not meant to be a production-grade traffic radar or anything — more of a learning project to understand object detection + tracking + basic physics working together.

## How It Works

1. The script loads the YOLOv8 model and opens a video (webcam or a video file).
2. Every frame gets resized down a bit, mainly so the display window fits nicely on screen and processing is a little faster.
3. YOLOv8 detects objects in the frame — cars, trucks, buses, people, etc.
4. Each detection is handed off to Norfair, which keeps track of the same object across multiple frames and gives it a consistent ID (so we don't lose track of "car #5" just because it moved a bit).
5. Two horizontal lines are drawn on the frame — Line 1 (closer to the camera or further, depending on your setup) and Line 2.
6. When a tracked vehicle's position crosses Line 1, the script notes down the frame number.
7. When that same vehicle later crosses Line 2, it checks how many frames passed and converts that into seconds using the video's FPS.
8. Speed is then just distance ÷ time:
   ```
   speed (m/s) = real_distance_meters / time_taken
   speed (km/h) = speed (m/s) × 3.6
   ```
9. The calculated speed is drawn above the vehicle on screen, and also printed to the console.

## Technologies Used

- **Python**
- **OpenCV** – reading the video, drawing lines/text, showing the output window
- **YOLOv8 (Ultralytics)** – detects vehicles and other objects in each frame
- **Norfair** – tracks detected objects across frames and assigns IDs
- **NumPy** – basic array/numeric handling for the detection points

## Configuration

Before running the script on your own video, there are a few values you'll need to adjust — these depend entirely on your camera angle and video resolution, so there's no one-size-fits-all setting:

- `red_line_1_y` / `red_line_2_y` — the pixel row (y-coordinate) where each line is drawn. These need to actually land on the road in your video, not on a building or the sky (yes, I learned this the hard way).
- `real_distance_meters` — the real-world distance between the two lines. This is the most important value for getting a realistic speed reading. I estimated mine using known reference sizes in the frame (like an average car being ~4.5m long, or a road lane being ~3-3.5m wide) since I didn't have exact GPS/survey data for the road.
- `DISPLAY_WIDTH` — how wide the video window is resized to. Adjust if it's too big or small for your screen.
- `cap = cv2.VideoCapture(...)` — set this to `0` for a webcam, or a file path for a video.
- `device="cpu"` or `device="cuda"` — CPU works everywhere but is slow. Only switch to `"cuda"` if you actually have an NVIDIA GPU with CUDA + a matching PyTorch build installed.

**Tip for finding line positions:** the script has a small built-in tool — click anywhere on the video window and it prints the pixel coordinates to the console. I used this to find exactly where the road was in my footage before setting the line values.

## A Note on Files Not Included in This Repo

Two things are intentionally **not** uploaded here:

- **The CCTV/traffic video** used for testing — it's someone else's footage/private recording, so I'm not including it. To use this project, just supply your own video file (or use a webcam) and point `cv2.VideoCapture(...)` to it.
- **`yolov8l.pt`** (the YOLOv8 model weights) — this file is fairly large and isn't something that needs to be tracked in git. It downloads automatically the first time you run the script, as long as `ultralytics` is installed.

## Running It

```bash
pip install opencv-python ultralytics norfair numpy
python Vehicle_Speed_Detection.py
```

Press `q` to close the window.

## Limitations (Being Honest Here)

- This only works well with a roughly straight-on camera view of the road. Steep rooftop angles distort distance, so speed readings won't be perfectly accurate.
- No perspective correction yet — it assumes the distance-per-pixel is the same across the whole frame, which isn't really true.
- Running on CPU is slow, expect maybe 1-3 frames per second with the large YOLOv8 model. A smaller model (`yolov8n.pt` or `yolov8s.pt`) helps if speed matters more than accuracy.
- Built for one-way traffic — doesn't currently handle vehicles crossing the lines in both directions.

## Ideas for Later

- Perspective transform for more accurate real-world distance mapping
- Support for multiple lanes at once
- Logging results to a CSV file instead of just the console
- Averaging speed over a few readings instead of a single crossing

