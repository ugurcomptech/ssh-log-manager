import re
from datetime import datetime
import pytz
import time
import os
import requests
import socket

LOG_FILE = "/var/log/auth.log"
SSH_SUCCESS_PATTERN = r"sshd\[[^\]]+\]: Accepted"
SSH_FAILURE_PATTERN = r"sshd\[[^\]]+\]: Failed"

seen_entries = set()
turkey_tz = pytz.timezone("Europe/Istanbul")
SERVER_URL = "http://:5000/log"  # BURAYA MERKEZİ SUNUCUNUN IP'SİNİ YAZ 

hostname = socket.gethostname()

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

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
        entry_key = f"{ip_address}-{status}-{username if username else ''}"
        if entry_key not in seen_entries:
            seen_entries.add(entry_key)
            send_to_server(ip_address, status, username)

def send_to_server(ip, status, username=None):
    data = {
        "ip": ip,
        "status": status,
        "username": username,
        "source": hostname
    }
    try:
        response = requests.post(SERVER_URL, json=data, timeout=3)
        if response.status_code != 200:
            print(f"[!] Hata ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Bağlantı hatası: {e}")

if __name__ == "__main__":
    with open(LOG_FILE, 'r') as logfile:
        loglines = follow(logfile)
        for line in loglines:
            process_line(line)
