# 🚗 Vehicle Identification Using YOLOv8

This project implements **YOLOv8** for real-time **vehicle detection and tracking** in images and videos. It can detect vehicles such as **cars, buses, and trucks** and track their movement across frames using a **custom tracking algorithm**.

## 🔥 Features
- **Image-Based Detection**: Detects and annotates vehicles in static images.
- **Video-Based Tracking**: Identifies and tracks moving vehicles in videos.
- **Custom Object Tracker**: Assigns unique IDs to detected vehicles and maintains tracking.
- **YOLOv8 Integration**: Uses **Ultralytics' YOLOv8 model** for accurate object detection.
- **Vehicle Counting**: Counts the number of detected vehicles in real-time.

## 📌 Dependencies
Ensure you have the necessary dependencies installed:
```bash
pip install ultralytics cvzone opencv-python pandas matplotlib
```

## 📂 Project Structure
```
📦 Vehicle-Detection-YOLOv8
├── Tracker.py          # Custom tracking class for vehicle detection
├── image_detection.py  # Detects vehicles in images
├── video_tracking.py   # Detects and tracks vehicles in videos
├── assets/             # Sample images/videos for testing
└── README.md           # Project documentation
```

## 🛠 How to Use
### 1️⃣ Image-Based Vehicle Detection
Upload an image and run the following command:
```bash
python image_detection.py --image path/to/image.jpg
```

### 2️⃣ Video-Based Vehicle Tracking
Upload a video and execute:
```bash
python video_tracking.py --video path/to/video.mp4
```

## 📊 Output
- **Bounding boxes** around detected vehicles.
- **Live vehicle count** displayed on the video.
- **Summary of detected vehicles** printed in the console.

## 🚀 Future Improvements
- Implement lane-wise vehicle counting.
- Optimize detection speed for real-time applications.
- Expand dataset for improved accuracy.

## 📜 References
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)

📩 **Contributions are welcome!** Feel free to open issues or submit pull requests for improvements.

