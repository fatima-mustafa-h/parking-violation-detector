import time
import cv2
import numpy as np
import json
import smtplib
from email.mime.text import MIMEText

violation_threshold = 60  # seconds before sending alert
violation_log = {}

def send_email_alert(zone_id, timestamp):
    sender = "your_email@example.com"
    receiver = "alert_receiver@example.com"
    msg = MIMEText(f"Parking violation detected in Zone {zone_id} at {timestamp}")
    msg['Subject'] = f"Violation Alert - Zone {zone_id}"
    msg['From'] = sender
    msg['To'] = receiver

    # Replace with your SMTP server details
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login("your_email@example.com", "your_password")
        server.sendmail(sender, receiver, msg.as_string())

def check_violations(zones, cars):
    global violation_log
    current_time = time.time()

    for zone_id, coords in zones.items():
        zone_violated = False
        for car_box in cars:
            x_center = int((car_box[0] + car_box[2]) / 2)
            y_center = int((car_box[1] + car_box[3]) / 2)
            if cv2.pointPolygonTest(coords.reshape((-1, 1, 2)), (x_center, y_center), False) >= 0:
                zone_violated = True
                if zone_id not in violation_log:
                    violation_log[zone_id] = current_time
                else:
                    start_time = violation_log[zone_id]
                    if (current_time - start_time) > violation_threshold:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        send_email_alert(zone_id, timestamp)
                        if 'alerts' not in violation_log:
                            violation_log['alerts'] = {}
                        if zone_id not in violation_log['alerts']:
                            violation_log['alerts'][zone_id] = []
                        violation_log['alerts'][zone_id].append(timestamp)
            else:
                if zone_id in violation_log:
                    violation_log.pop(zone_id)

def save_violation_log(filepath='violation_log.json'):
    with open(filepath, 'w') as f:
        json.dump(violation_log, f)

# In your main detection loop in parking_violation.py:

# 1. Load zones from zones.yaml (done elsewhere)
# 2. Detect cars bounding boxes with your detector (YOLOv8 or other)
# 3. Call check_violations(zones, detected_cars)
# 4. Periodically call save_violation_log()

# Example minimal main loop structure:

# zones = load_zones()  # your zones loaded as {zone_id: np.array(coords)}
# while True:
#     frame = get_next_frame()
#     cars = detect_cars(frame)  # list of [x1,y1,x2,y2]
#     check_violations(zones, cars)
#     save_violation_log()

