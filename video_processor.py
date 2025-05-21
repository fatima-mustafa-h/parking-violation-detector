import threading
import time
import cv2
import numpy as np
from shapely.geometry import Polygon, box as shapely_box
from ultralytics import YOLO
from email_utils import send_email_alert

class VideoProcessor:
    def __init__(self):
        self.no_parking_zones = []  # List of shapely Polygons
        self.violations = []        # List of dicts with violation info
        self.lock = threading.Lock()
        self.frame = None
        self.capture = None
        self.running = False
        self.model = YOLO('yolov8n.pt')  # Use YOLOv8 nano model
        self.alerted_violations = set()  # To prevent duplicate alerts

    def set_no_parking_zones(self, zones):
        with self.lock:
            self.no_parking_zones = [Polygon(zone) for zone in zones]

    def start_capture(self, source=0):
        self.capture = cv2.VideoCapture(source)
        self.running = True
        threading.Thread(target=self._process_frames, daemon=True).start()

    def _process_frames(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                time.sleep(0.1)
                continue
            with self.lock:
                self.frame = frame.copy()
            self._detect_violations(frame)
            time.sleep(0.03)

    def _detect_violations(self, frame):
        results = self.model(frame)
        violations_found = []

        for r in results:
            if not hasattr(r, "boxes") or r.boxes is None:
                continue
            for box_data in r.boxes.xyxy.cpu().numpy():
                x1, y1, x2, y2 = box_data
                vehicle_box = shapely_box(x1, y1, x2, y2)
                for zone_idx, polygon in enumerate(self.no_parking_zones):
                    if polygon.intersects(vehicle_box):
                        violation_id = (zone_idx, int(x1), int(y1), int(x2), int(y2))
                        with self.lock:
                            if violation_id not in self.alerted_violations:
                                self.violations.append({
                                    'zone': zone_idx,
                                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                                    'time': time.strftime("%Y-%m-%d %H:%M:%S"),
                                })
                                self.alerted_violations.add(violation_id)
                                threading.Thread(target=send_email_alert, args=(
                                    "Parking Violation Detected",
                                    f"Violation detected in zone {zone_idx} at {time.strftime('%Y-%m-%d %H:%M:%S')}",
                                    "recipient_email@example.com"
                                ), daemon=True).start()
                        violations_found.append(violation_id)

        with self.lock:
            self.alerted_violations = {v for v in self.alerted_violations if v in violations_found}

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            if not ret:
                return None
            return jpeg.tobytes()

    def get_all_violations(self):
        with self.lock:
            return list(self.violations)

    def stop(self):
        self.running = False
        if self.capture:
            self.capture.release()
