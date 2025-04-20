import re
from datetime import datetime
import pytz
import time
import os
from threading import Thread
from flask import Flask, request

LOG_FILE = "/var/log/auth.log"
LOG_DIR = "/var/log"  # Günlük loglar burada olacak

SSH_SUCCESS_PATTERN = r"sshd\[[^\]]+\]: Accepted"
SSH_FAILURE_PATTERN = r"sshd\[[^\]]+\]: Failed"

seen_entries = set()
turkey_tz = pytz.timezone("Europe/Istanbul")
app = Flask(__name__)  # Flask server

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def get_log_file_path():
    today = datetime.now(turkey_tz).strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"ssh_{today}.log")

def write_log(ip_address, status, username=None, source="local"):
    now_tr = datetime.now(turkey_tz)
    timestamp = now_tr.strftime("%b %d %H:%M")
    entry_key = f"{source}-{ip_address}-{status}-{username if username else ''}"

    if entry_key not in seen_entries:
        seen_entries.add(entry_key)
        if username:
            log_entry = f"{timestamp} - {ip_address} - {status} - user: {username} - source: {source}\n"
        else:
            log_entry = f"{timestamp} - {ip_address} - {status} - source: {source}\n"

        log_file_path = get_log_file_path()
        with open(log_file_path, 'a') as output_file:
            output_file.write(log_entry)
        print(log_entry.strip())

def process_line(line):
    status = None
    username = None
    ip_address = None

    if re.search(SSH_SUCCESS_PATTERN, line):
        status = "Success"
        match = re.search(r'Accepted .* for (\w+) from (\S+)', line)
        if match:
            username = match.group(1)
            ip_address = match.group(2)
        else:
            return

    elif re.search(SSH_FAILURE_PATTERN, line):
        status = "Failure"
        match = re.search(r'from (\S+)', line)
        if match:
            ip_address = match.group(1)

    if status and ip_address:
        write_log(ip_address, status, username)

@app.route("/log", methods=["POST"])
def receive_remote_log():
    data = request.json
    ip = data.get("ip")
    status = data.get("status")
    username = data.get("username")
    source = data.get("source", "remote")

    if ip and status:
        write_log(ip, status, username, source)
        return "OK", 200
    else:
        return "Missing data", 400

def start_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    Thread(target=start_flask, daemon=True).start()  # Flask arka planda çalışacak

    current_day = datetime.now(turkey_tz).day

    with open(LOG_FILE, 'r') as logfile:
        loglines = follow(logfile)
        for line in loglines:
            now_day = datetime.now(turkey_tz).day
            if now_day != current_day:
                current_day = now_day
                seen_entries.clear()
            process_line(line)
