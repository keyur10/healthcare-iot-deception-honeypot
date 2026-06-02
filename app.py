from pathlib import Path
from collections import Counter
from functools import wraps
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
    abort,
)

# ==================================================
# APP CONFIG
# ==================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "soc-dashboard-secret"
)

BASE_DIR = Path(__file__).resolve().parent

LOG_FILE = (
    BASE_DIR /
    "logs" /
    "cowrie.json"
)

# ==================================================
# TEST USERS (NO DATABASE YET)
# ==================================================

USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
    },
    "analyst": {
        "password": "analyst123",
        "role": "analyst",
    },
    "viewer": {
        "password": "viewer123",
        "role": "viewer",
    },
}

# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ==================================================
# AUTH HELPERS
# ==================================================

def is_authenticated():

    return bool(
        session.get("user")
    )


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not is_authenticated():

            return redirect(
                url_for("login")
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper


def role_required(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if not is_authenticated():

                return redirect(
                    url_for("login")
                )

            if (
                session.get("role")
                not in roles
            ):
                abort(403)

            return func(
                *args,
                **kwargs
            )

        return wrapper

    return decorator

# ==================================================
# DASHBOARD HELPERS
# ==================================================

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

    except Exception as error:

        logger.error(error)

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
# HOME
# ==================================================

@app.route("/")
def home():

    if is_authenticated():

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
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
            url_for("dashboard")
        )

    if request.method == "POST":

        username = (
            request.form.get(
                "username",
                ""
            ).strip()
        )

        password = (
            request.form.get(
                "password",
                ""
            ).strip()
        )

        user = USERS.get(
            username
        )

        if (
            user
            and user["password"]
            == password
        ):

            session["user"] = (
                username
            )

            session["role"] = (
                user["role"]
            )

            flash(
                "Login successful",
                "success",
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        flash(
            "Invalid credentials",
            "danger",
        )

    return render_template(
        "login.html"
    )


@app.route("/logout")
@login_required
def logout():

    session.clear()

    flash(
        "Logged out",
        "info",
    )

    return redirect(
        url_for("login")
    )

# ==================================================
# MAIN PAGES
# ==================================================

@app.route("/dashboard")
@login_required
def dashboard():

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


@app.route("/about")
@login_required
def about():

    return render_template(
        "about.html"
    )

# ==================================================
# SOC MODULES
# ==================================================

@app.route("/alerts")
@login_required
def alerts():
    return render_template("alerts.html")


@app.route("/attack-logs")
@login_required
def attack_logs():
    return render_template("attack_logs.html")


@app.route("/attack-statistics")
@login_required
def attack_statistics():
    return render_template(
        "attack_statistics.html"
    )


@app.route("/attack-timeline")
@login_required
def attack_timeline():
    return render_template(
        "attack_timeline.html"
    )


@app.route("/geolocation")
@login_required
def geolocation():
    return render_template(
        "geolocation.html"
    )


@app.route("/reports")
@login_required
def reports():
    return render_template(
        "reports.html"
    )

# ==================================================
# ANALYST + ADMIN
# ==================================================

@app.route("/ioc-extraction")
@role_required(
    "admin",
    "analyst"
)
def ioc_extraction():
    return render_template(
        "ioc_extraction.html"
    )


@app.route("/malware-analysis")
@role_required(
    "admin",
    "analyst"
)
def malware_analysis():
    return render_template(
        "malware_analysis.html"
    )


@app.route("/mitre-mapping")
@role_required(
    "admin",
    "analyst"
)
def mitre_mapping():
    return render_template(
        "mitre_mapping.html"
    )


@app.route("/threat-classification")
@role_required(
    "admin",
    "analyst"
)
def threat_classification():
    return render_template(
        "threat_classification.html"
    )


@app.route("/threat-hunting")
@role_required(
    "admin",
    "analyst"
)
def threat_hunting():
    return render_template(
        "threat_hunting.html"
    )


@app.route("/case-management")
@role_required(
    "admin",
    "analyst"
)
def case_management():
    return render_template(
        "case_management.html"
    )


@app.route("/incident-response")
@role_required(
    "admin",
    "analyst"
)
def incident_response():
    return render_template(
        "incident_response.html"
    )

# ==================================================
# ALL USERS
# ==================================================

@app.route("/ip-intelligence")
@login_required
def ip_intelligence():
    return render_template(
        "ip_intelligence.html"
    )


@app.route("/asset-inventory")
@login_required
def asset_inventory():
    return render_template(
        "asset_inventory.html"
    )

# ==================================================
# ADMIN ONLY
# ==================================================

@app.route("/settings")
@role_required("admin")
def settings():
    return render_template(
        "settings.html"
    )


@app.route("/user-management")
@role_required("admin")
def user_management():
    return render_template(
        "user_management.html"
    )


@app.route("/audit-logs")
@role_required("admin")
def audit_logs():
    return render_template(
        "audit_logs.html"
    )

# ==================================================
# API
# ==================================================

@app.route("/api/stats")
@login_required
def api_stats():

    return jsonify(
        get_attack_data()
    )


@app.route("/api/recent")
@login_required
def api_recent():

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
            "status": "healthy",
            "service": "soc-platform",
        }
    )

# ==================================================
# STATUS
# ==================================================

@app.route("/status")
@login_required
def status():

    stats = get_attack_data()

    return render_template(
        "status.html",
        stats=stats,
    )

# ==================================================
# ERROR HANDLERS
# ==================================================

@app.errorhandler(403)
def forbidden(error):

    return (
        render_template(
            "error.html",
            error_code="403",
            error_title="Forbidden",
            error_message="ACCESS DENIED",
            error_description="Permission denied.",
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
            error_description="Page does not exist.",
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
            error_description="Unexpected application error.",
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