import csv
import os


def export_attack_report(data, filename):

    os.makedirs("reports", exist_ok=True)

    filepath = f"reports/{filename}"

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "IP Address",
            "Username",
            "Password",
            "Timestamp"
        ])

        for attack in data:

            writer.writerow([
                attack.get("ip"),
                attack.get("username"),
                attack.get("password"),
                attack.get("timestamp")
            ])

    return filepath