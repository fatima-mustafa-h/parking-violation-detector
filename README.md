
# Parking Violation Detector

This project detects illegal parking in user-defined no-parking zones using YOLOv8 object detection. It supports both live CCTV feeds and uploaded video files. A real-time dashboard displays violations, durations, and analytics.

---

## Features

- **Dynamic No-Parking Zone Marking** via web UI  
- **Real-Time Violation Detection** using pre-trained YOLOv8  
- **Violation Time Tracking and Alerts**   
- **Firebase Firestore Authentication (Signup/Login)**  
- **Violation Dashboard with Analytics**  
- **Email Notifications**

---

## Installation

```bash
git clone git@github.com:fatima-mustafa-h/parking-violation-detector.git
cd parking-violation-detector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
---

## Usage

```bash
python app.py
```
Open http://127.0.0.1:5000 in your browser.

---

## Folder Structure

```bash
.
├── app/                  # Flask app backend
├── templates/            # HTML files
├── static/               # CSS, JS, images
├── yolo/                 # Detection model logic
├── utils/                # Zone marking, time tracking
├── test_videos/          # Sample inputs
├── requirements.txt
├── app.py                # Entry point
└── README.md
```
---

## Firebase Setup

- Create a Firebase project
- Enable Firestore and Authentication
- Add your config to firebase_config.js in static/

---

## License

MIT License. See LICENSE file.
