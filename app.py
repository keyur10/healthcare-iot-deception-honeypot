# app.py

from pathlib import Path
from collections import Counter
import json
import logging
import os

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

# ==================================================
# CONFIG
# ==================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "change-this-secret-key"
)

BASE_DIR = Path(__file__).resolve().parent

LOG_FILE = (
    BASE_DIR /
    "logs" /
    "cowrie.json"
)

ADMIN_USER = os.getenv(
    "ADMIN_USER",
    "admin"
)

ADMIN_PASSWORD = os.getenv(
    "ADMIN_PASSWORD",
    "admin123"
)

# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==================================================
# HELPERS
# ==================================================


def is_authenticated() -> bool:
    return bool(session.get("user"))


def calculate_threat_level(
    total_attacks: int
) -> str:

    if total_attacks >= 500:
        return "CRITICAL"

    if total_attacks >= 250:
        return "HIGH"

    if total_attacks >= 100:
        return "MEDIUM"

    return "LOW"


def get_attack_data() -> dict:

    attacks = []

    unique_ips = set()

    country_counter = Counter()

    if not LOG_FILE.exists():

        logger.warning(
            "Cowrie log file not found"
        )

        return {
            "total_attacks": 0,
            "unique_ips": 0,
            "recent_attacks": [],
            "country_stats": [],
            "threat_level": "LOW",
        }

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:

                    data = json.loads(line)

                    ip = data.get(
                        "src_ip",
                        "Unknown"
                    )

                    attack = {
                        "ip": ip,
                        "username": data.get(
                            "username",
                            "N/A",
                        ),
                        "password": data.get(
                            "password",
                            "N/A",
                        ),
                        "timestamp": data.get(
                            "timestamp",
                            "N/A",
                        ),
                    }

                    attacks.append(
                        attack
                    )

                    unique_ips.add(ip)

                    country = data.get(
                        "country",
                        "Unknown"
                    )

                    country_counter[
                        country
                    ] += 1

                except json.JSONDecodeError:
                    continue

    except OSError as error:

        logger.error(
            "Error reading log file: %s",
            error,
        )

    total_attacks = len(attacks)

    country_stats = [
        {
            "country": country,
            "count": count,
        }
        for country, count in
        country_counter.most_common(10)
    ]

    return {
        "total_attacks": total_attacks,
        "unique_ips": len(unique_ips),
        "recent_attacks": attacks[-20:][::-1],
        "country_stats": country_stats,
        "threat_level":
            calculate_threat_level(
                total_attacks
            ),
    }


# ==================================================
# ROUTES
# ==================================================


@app.route("/")
def home():

    if is_authenticated():

        return redirect(
            url_for(
                "dashboard"
            )
        )

    return redirect(
        url_for(
            "login"
        )
    )


# ==================================================
# LOGIN
# ==================================================


@app.route(
    "/login",
    methods=["GET", "POST"],
)
def login():

    if is_authenticated():

        return redirect(
            url_for(
                "dashboard"
            )
        )

    if request.method == "POST":

        username = (
            request.form.get(
                "username",
                "",
            )
            .strip()
        )

        password = (
            request.form.get(
                "password",
                "",
            )
            .strip()
        )

        if (
            username == ADMIN_USER
            and password ==
            ADMIN_PASSWORD
        ):

            session["user"] = username

            flash(
                "Login successful",
                "success",
            )

            logger.info(
                "User logged in: %s",
                username,
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        flash(
            "Invalid username or password",
            "danger",
        )

    return render_template(
        "login.html"
    )


@app.route("/logout")
def logout():

    username = session.get(
        "user"
    )

    session.clear()

    logger.info(
        "User logged out: %s",
        username,
    )

    flash(
        "Logged out successfully",
        "info",
    )

    return redirect(
        url_for(
            "login"
        )
    )


# ==================================================
# DASHBOARD
# ==================================================


@app.route("/dashboard")
def dashboard():

    if not is_authenticated():

        return redirect(
            url_for(
                "login"
            )
        )

    stats = get_attack_data()

    return render_template(
        "dashboard.html",
        total_attacks=stats[
            "total_attacks"
        ],
        unique_ips=stats[
            "unique_ips"
        ],
        recent_attacks=stats[
            "recent_attacks"
        ],
        country_stats=stats[
            "country_stats"
        ],
        threat_level=stats[
            "threat_level"
        ],
    )


# ==================================================
# ABOUT
# ==================================================


@app.route("/about")
def about():

    if not is_authenticated():

        return redirect(
            url_for(
                "login"
            )
        )

    return render_template(
        "about.html"
    )


# ==================================================
# API
# ==================================================


@app.route("/api/stats")
def api_stats():

    if not is_authenticated():

        return jsonify(
            {
                "error":
                "Unauthorized"
            }
        ), 401

    return jsonify(
        get_attack_data()
    )


@app.route("/api/recent")
def api_recent():

    if not is_authenticated():

        return jsonify(
            {
                "error":
                "Unauthorized"
            }
        ), 401

    stats = get_attack_data()

    return jsonify(
        {
            "recent_attacks":
            stats[
                "recent_attacks"
            ]
        }
    )


@app.route("/api/health")
def api_health():

    return jsonify(
        {
            "status":
            "healthy",
            "service":
            "cowrie-dashboard",
        }
    )


# ==================================================
# STATUS
# ==================================================


@app.route("/status")
def status():

    stats = get_attack_data()

    return jsonify(
        {
            "project":
            "Healthcare IoT Deception Honeypot Network",

            "honeypot":
            "Cowrie",

            "dashboard":
            "Running",

            "status":
            "Active",

            "threat_level":
            stats[
                "threat_level"
            ],

            "total_attacks":
            stats[
                "total_attacks"
            ],

            "unique_ips":
            stats[
                "unique_ips"
            ],

            "log_file":
            str(LOG_FILE),
        }
    )


# ==================================================
# ERRORS
# ==================================================


@app.errorhandler(401)
def unauthorized(error):

    return (
        render_template(
            "error.html",
            error_code="401",
            error_title="Unauthorized",
            error_message="LOGIN REQUIRED",
            error_description=(
                "Authentication required."
            ),
        ),
        401,
    )


@app.errorhandler(403)
def forbidden(error):

    return (
        render_template(
            "error.html",
            error_code="403",
            error_title="Forbidden",
            error_message="ACCESS DENIED",
            error_description=(
                "Permission denied."
            ),
        ),
        403,
    )


@app.errorhandler(404)
def not_found(error):

    return (
        render_template(
            "error.html",
            error_code="404",
            error_title="Page Not Found",
            error_message="NOT FOUND",
            error_description=(
                "The requested page does not exist."
            ),
        ),
        404,
    )


@app.errorhandler(500)
def server_error(error):

    return (
        render_template(
            "error.html",
            error_code="500",
            error_title="Server Error",
            error_message="SERVER ERROR",
            error_description=(
                "Unexpected application error."
            ),
        ),
        500,
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )