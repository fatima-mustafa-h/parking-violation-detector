import cv2

class CameraStream:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture("rtsp://user:pass@IP:554/your_path")

    def generate(self):
       while True:
        frame = self.get_frame()
        if frame is None:
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # restart video
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to read frame")
                return None
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            print("Failed to encode frame")
            return None
        return jpeg.tobytes()

camera_stream = CameraStream()
