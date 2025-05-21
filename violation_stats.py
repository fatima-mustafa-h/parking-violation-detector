import json
from collections import Counter
from datetime import datetime

def load_violations(path='violation_log.json'):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

def analyze_violations(log_data):
    zone_counts = {zone: len(times) for zone, times in log_data.items()}
    all_times = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for times in log_data.values() for ts in times]
    hourly_distribution = Counter([dt.hour for dt in all_times])
    return zone_counts, dict(hourly_distribution)

def main():
    log_data = load_violations()
    zone_counts, hourly_distribution = analyze_violations(log_data)

    print("Most Violated Zones:")
    for zone, count in sorted(zone_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"Zone {zone}: {count} violations")

    print("\nViolation Peak Hours:")
    for hour, count in sorted(hourly_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"{hour}:00 - {hour}:59 : {count} violations")

if __name__ == '__main__':
    main()
