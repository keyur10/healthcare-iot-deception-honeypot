import json
import os

LOG_FILE = "logs/cowrie.json"

def get_attack_logs():

    attacks = []

    try:

        print("Looking for:", os.path.abspath(LOG_FILE))

        with open(LOG_FILE, "r") as file:

            for line in file:

                line = line.strip()

                if line:

                    attack = json.loads(line)

                    attacks.append({

                        "time": attack.get("timestamp", "Unknown"),
                        "ip": attack.get("src_ip", "Unknown"),
                        "username": attack.get("username", "Unknown"),
                        "password": attack.get("password", "Unknown")

                    })

    except Exception as e:

        print("Error:", e)

    return attacks


