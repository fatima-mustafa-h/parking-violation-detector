from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from auth import auth_blueprint, firebase_app, init_firebase
from video_processor import VideoProcessor
from camera_stream import CameraStream
from analytics import get_violation_stats
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(auth_blueprint)

init_firebase()

video_processor = VideoProcessor()
camera_stream = CameraStream(0)


@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')

@app.route('/violations')
def violations():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    violations = video_processor.get_all_violations()
    return render_template('violations.html', violations=violations)

@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    stats = get_violation_stats()
    return render_template('analytics.html', stats=stats)

@app.route('/live_feed')
def live_feed():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('live_feed.html')

@app.route('/video_feed')
def video_feed():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return Response(camera_stream.generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/set_zones', methods=['POST'])
def set_zones():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    zones = request.json.get('zones', [])
    video_processor.set_no_parking_zones(zones)
    return jsonify({"status": "Zones updated"})

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
