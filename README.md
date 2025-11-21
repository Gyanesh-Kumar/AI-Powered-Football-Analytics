# AI Powered Football Analytics

This repository contains a complete **AI-based football analytics system** that performs player detection, tracking, team assignment, ball tracking, speed estimation, camera motion compensation, and visualization. The system processes full-match video footage and extracts advanced analytics useful for coaches, analysts, and automation pipelines.

---

## 🚀 Features

### **1. Player, Referee, and Ball Detection**

* Uses **YOLOv5** for real-time object detection.
* Trained on football-specific datasets.
* Labels include: `ball`, `player`, `goalkeeper`, `referee`.

### **2. Multi-Object Tracking (MOT)**

* Implements **ByteTrack** to associate detections across frames.
* Assigns stable `track_id` values for players and the ball.
* Handles occlusions and re-identification.

### **3. Camera Movement Estimation**

* Optical flow–based estimation to differentiate **player motion** vs **camera motion**.
* Ensures accurate distance & speed estimation.

### **4. Team Assignment**

* Uses **K-Means clustering** on cropped jersey colors.
* Separates players into Team A and Team B.
* Works even with similar kits.

### **5. Ball Possession Assignment**

* Detects ball proximity to players.
* Determines which player currently controls the ball.
* Handles edge cases (e.g., ball mid-air).

### **6. View Transformation & Real-World Metrics**

* Applies perspective transforms to convert pixel movement → meters.
* Estimates:

  * **Player speed (km/h)**
  * **Distance covered (meters)**

### **7. Output Visualizations**

* Draws bounding boxes, IDs, jersey numbers.
* Draws ball trajectory.
* Saves annotated output as a video.

---

## 📁 Project Structure

```
AI Powered Football Analytics/
│
├── camera_movement_estimator/
├── development_and_analysis/
├── football-players-detection-1/
├── input_videos/               # (User will place input videos here)
├── models/                     # (User will place YOLO model here)
├── output_videos/              # (Annotated video output generated)
├── player_ball_assigner/
├── speed_and_distance_estimator/
├── team_assigner/
├── trackers/
├── utils/
├── view_transformer/
│
├── main.py                     # Main execution file
├── yolo_inference.py
├── req.txt                     # Dependencies
└── README.md                   # This file
```

---

## 📦 Installation

### **1. Clone the repository**

```bash
git clone https://github.com/Gyanesh-Kumar/AI-Powered-Football-Analytics.git
cd AI Powered Football Analytics
```

### **2. Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### **3. Install dependencies**

```bash
pip install -r req.txt
```

---

## 📥 Download Required Assets

You need to upload the following files manually:

### **1. YOLO Model (`best.pt`)**

Create the folder:

```bash
mkdir models
```

Place your model here:

```
models/best.pt
```

### **2. Input Video(s)**

Create the folder:

```bash
mkdir input_videos
```

Place your raw match footage here:

```
input_videos/input.mp4
```

### **3. Output Videos Folder**

Create the folder:

```bash
mkdir output_videos
```

The system will automatically write processed videos here.

---

## ▶️ Running the System

Run the following command:

```bash
python main.py
```

This will:

* Load YOLO model
* Detect and track players, referees, and ball
* Assign teams
* Estimate speed and distance
* Draw overlays
* Save output video to `output_videos/`

---

## 📊 Output

The system generates:

### ✔ Annotated video

* Bounding boxes
* Player IDs
* Team color overlays
* Ball trajectory

### ✔ JSON files

* Player tracks
* Ball tracks
* Speed & distance
* Team assignments

All stored in the `stubs/` directory.

---

## 🧠 Technologies Used

* **Python 3.9**
* **OpenCV**
* **YOLOv5** (PyTorch)
* **ByteTrack**
* **NumPy / SciPy**
* **K-Means Clustering**
* **Optical Flow (Lucas-Kanade)**

---

## 📌 Notes

* Heavy files (model, videos) are intentionally **not included** in GitHub.
* Ensure your `models/`, `input_videos/`, and `output_videos/` folders exist.
* The system can process any 720p/1080p match footage.

---

## 📈 Possible Future Improvements

* Pose estimation for players
* Event detection: passes, shots, fouls
* Heatmaps & possession analysis
* Web UI for easier demo

---

## 🏆 Author

**Gyanesh Kumar**


If you find this project useful, feel free to ⭐ star the repo!
