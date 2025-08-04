import csv
import json
from datetime import datetime

def log_event(message):
    timestamp = datetime.now().isoformat()
    log_data = {"timestamp": timestamp, "message": message}

    # Append to CSV
    with open("outputs/logs.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, message])

    # Append to JSON
    try:
        with open("outputs/report.json", "r") as f:
            existing = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        existing = []

    existing.append(log_data)

    with open("outputs/report.json", "w") as f:
        json.dump(existing, f, indent=4)
