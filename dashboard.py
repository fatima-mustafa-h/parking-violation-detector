from flask import Flask, jsonify, render_template
import json
from collections import Counter
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/violations')
def get_violations():
    with open('violation_log.json', 'r') as file:
        data = json.load(file)

    violations = data.get("violations", [])
    total = len(violations)
    zone_counts = Counter(v["zone_id"] for v in violations)
    time_counts = Counter(datetime.fromisoformat(v["timestamp"]).hour for v in violations)

    most_common_zone = zone_counts.most_common(1)[0][0] if zone_counts else "N/A"
    peak_hour = time_counts.most_common(1)[0][0] if time_counts else "N/A"

    analytics = {
        "total_violations": total,
        "violations_per_zone": dict(zone_counts),
        "most_violated_zone": most_common_zone,
        "peak_hour": peak_hour
    }

    return jsonify({
        "violations": violations,
        "analytics": analytics
    })

if __name__ == '__main__':
    app.run(debug=True)

