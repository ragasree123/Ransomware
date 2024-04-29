import re
from datetime import datetime
from mitigate import terminate_processes

def parse_log_entries(filename):
    # Read the log file
    with open(filename, 'r') as file:
        log_entries = file.readlines()

    events = []
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - File (.*?) has been (created|modified)")
    for entry in log_entries:
        match = pattern.search(entry)
        if match:
            timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
            file_path = match.group(2)
            event_type = match.group(3)
            events.append((timestamp, file_path, event_type))
    return events

def detect_ransomware_activity(events):
    alerts = []
    for timestamp, file_path, event_type in events:
        if '.enc' in file_path:
            alert_message = f"Alert: Suspicious {event_type} detected: {file_path} at {timestamp}"
            alerts.append(alert_message)
            terminate_processes("suspicious_process")

    return alerts

def write_alerts_to_file(alerts, alert_file='alerts_log.txt'):
    with open(alert_file, 'w') as file:
        for alert in alerts:
            file.write(f"{alert}\n")

if __name__ == "__main__":
    log_file_path = 'fim_log.txt'
    events = parse_log_entries(log_file_path)
    detected_alerts = detect_ransomware_activity(events)

    # Print alerts to console
    for alert in detected_alerts:
        print(alert)

    # Write alerts to a file
    write_alerts_to_file(detected_alerts)
