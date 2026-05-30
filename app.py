from pathlib import Path
import json

from flask import Flask, jsonify, render_template

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "logs" / "cowrie.json"


def get_attack_data() -> dict:
    attack_count = 0
    unique_ips = set()
    recent_attacks = []

    if not LOG_FILE.exists():
        return {
            "total_attacks": 0,
            "unique_ips": 0,
            "recent_attacks": [],
        }

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                try:
                    data = json.loads(line)

                    attack_count += 1

                    attack = {
                        "ip": data.get("src_ip", "Unknown"),
                        "username": data.get("username", "N/A"),
                        "password": data.get("password", "N/A"),
                        "timestamp": data.get("timestamp", "N/A"),
                    }

                    unique_ips.add(attack["ip"])
                    recent_attacks.append(attack)

                except json.JSONDecodeError:
                    continue

    except OSError as error:
        print(f"Error reading log file: {error}")

    return {
        "total_attacks": attack_count,
        "unique_ips": len(unique_ips),
        "recent_attacks": recent_attacks[-10:][::-1],
    }


@app.route("/")
def dashboard():
    stats = get_attack_data()

    return render_template(
        "dashboard.html",
        total_attacks=stats["total_attacks"],
        unique_ips=stats["unique_ips"],
        recent_attacks=stats["recent_attacks"],
    )


@app.route("/api/stats")
def api_stats():
    return jsonify(get_attack_data())


@app.route("/status")
def status():
    return jsonify(
        {
            "project": "Healthcare IoT Deception Honeypot Network",
            "honeypot": "Cowrie",
            "dashboard": "Running",
            "status": "Active",
            "log_file": str(LOG_FILE),
        }
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )