import json
import os
from datetime import datetime

AUDIT_FILE = "data/audit_logs.json"


def log_action(user, action):

    log_entry = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "user": user,
        "action": action
    }

    logs = []

    if os.path.exists(AUDIT_FILE):

        with open(AUDIT_FILE, "r") as file:

            try:
                logs = json.load(file)
            except:
                logs = []

    logs.append(log_entry)

    with open(AUDIT_FILE, "w") as file:
        json.dump(logs, file, indent=4)


def get_logs():

    if not os.path.exists(AUDIT_FILE):
        return []

    with open(AUDIT_FILE, "r") as file:
        return json.load(file)