# 🎧 Headphones-Controlled Video Playback

This project uses real-time computer vision to detect whether you’re wearing headphones and automatically plays or pauses a YouTube or local video for you — no hands needed!

Sometimes I take small breaks watching YouTube while working. Instead of manually hitting the play/pause button, I trained a YOLOv8 model to do it for me 😄.

---

## 🧠 How It Works

- **YOLOv8 Custom Model** trained to detect two classes:
  - `headphones_on`
  - `headphones_off`
- **OpenCV** processes live webcam feed and runs YOLO inference
- **PyAutoGUI** simulates mouse clicks based on detection
- Works in real-time 

---

## 🛠️ Tech Stack

| Component       | Description                              |
|----------------|------------------------------------------|
| Python          | Core programming language                |
| YOLOv8 (Ultralytics) | Object detection model             |
| OpenCV          | Webcam input and display window          |
| PyAutoGUI       | Mouse control automation                 |
| ffmpeg          | (optional) For converting videos for compatibility |

---

## 📦 Installation

```bash
# Create a new environment (optional but recommended)
conda create -n headphones python=3.10
```
```bash
conda activate headphones
```

# Clone the repo
```bash
git clone https://github.com/yourusername/headphone-control.git
```
```bash
cd headphone-control
```

# Install dependencies
```bash
pip install -r requirements.txt
```
