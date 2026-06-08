import json
from collections import Counter

def hunt_threats():

    ips = []
    passwords = []

    try:

        with open("data/cowrie.json", "r") as file:

            for line in file:

                attack = json.loads(line)

                ips.append(
                    attack["src_ip"]
                )

                passwords.append(
                    attack["password"]
                )

    except Exception:
        pass

    return {

        "total_hunts": len(ips),

        "top_ips":
        Counter(ips).most_common(10),

        "top_passwords":
        Counter(passwords).most_common(10)

    }