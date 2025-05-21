import cv2
import json
import time
import os

def process_video(video_path):
    # Placeholder for video processing logic
    # Implement your parking violation detection here
    # For demonstration, we'll just simulate processing time
    time.sleep(5)
    # Log a dummy violation
    violation = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "video": video_path
    }
    if not os.path.exists('violation_log.json'):
        with open('violation_log.json', 'w') as f:
            json.dump([], f)
    with open('violation_log.json', 'r+') as f:
        data = json.load(f)
        data.append(violation)
        f.seek(0)
        json.dump(data, f, indent=4)

