from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from core.config import APP
from ipwhois import IPWhois
import json

USERS_FILE = "users.json"


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

from core.config import (
    APP,
    SECRET_KEY,
    PROJECT_NAME,
)

from core.helpers import (
    configure_logging,
)

from core.storage import (
    ensure_data_files,
)

from core.auth import (
    login_user,
    logout_user,
    is_authenticated,
    current_user,
    current_role,
)

from core.audit import (
    log_event,
)

# ==================================================
# APP
# ==================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY


# ==================================================
# STARTUP
# ==================================================

def initialize_app() -> None:

    configure_logging()

    ensure_data_files()

    log_event(
        event_type="SYSTEM",
        message="Application started",
        severity="INFO",
    )


initialize_app()


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

    if request.method == "POST":

        username = request.form.get(
            "username",
            "",
        )

        password = request.form.get(
            "password",
            "",
        )

        if login_user(
            username,
            password,
        ):

            flash(
                "Login successful",
                "success",
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid credentials",
            "danger",
        )

    return render_template(
    "auth/login.html",
    project_name=PROJECT_NAME,
)


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("login")
    )


# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    honeypots = load_honeypots()

    active_honeypots = len(
        [h for h in honeypots
         if h["status"] == "Active"]
    )

    return render_template(
        "dashboard/dashboard.html",
        active_honeypots=active_honeypots
    )
@app.route(
    "/whois",
    methods=["POST"]
)
def whois_lookup():

    ip = request.form.get("ip")

    result = None

    try:

        lookup = IPWhois(ip)

        data = lookup.lookup_rdap()

        result = {
            "ip": ip,
            "country": data.get("asn_country_code"),
            "asn": data.get("asn"),
            "provider": data.get("network", {}).get("name"),
            "city": "Unknown",
        }

    except Exception:

        result = {
            "ip": ip,
            "country": "Unknown",
            "asn": "Unknown",
            "provider": "Unknown",
            "city": "Unknown",
        }

    return render_template(
        "dashboard/dashboard.html",
        whois_result=result,
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/mitre")
def mitre():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/mitre_mapping.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
# ==================================================
# ATTACK LOGS
# ==================================================

@app.route("/attack-logs")
def attack_logs():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/attack_logs.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/threat-hunting")
def threat_hunting():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/threat_hunting.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )

@app.route("/alerts")
def alerts():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/alerts.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/timeline")
def timeline():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/timeline.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/geolocation")
def geolocation():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/geolocation.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
# ==================================================
# IOC EXTRACTION
# ==================================================

@app.route("/ioc")
def ioc_extraction():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/ioc_extraction.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
# ==================================================
# HONEYPOTS
# ==================================================

@app.route("/honeypots")
def honeypots():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/honeypots.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
# ==================================================
# DEVICES
# ==================================================

@app.route("/devices")
def devices():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/devices.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/reports")
def reports():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/reports.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/settings")
def settings():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/settings.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/settings/user-management")
def user_management():

    users = load_users()

    total_users = len(users)

    admins = sum(
        1 for user in users
        if user.get("role") == "Administrator"
    )

    analysts = sum(
        1 for user in users
        if user.get("role") == "Threat Analyst"
    )

    disabled_accounts = sum(
        1 for user in users
        if user.get("status") == "Disabled"
    )

    return render_template(
    "dashboard/user_management.html",
    users=users,
    total_users=total_users,
    admins=admins,
    analysts=analysts,
    disabled_accounts=disabled_accounts
)
@app.route("/add-user", methods=["POST"])
def add_user():

    users = load_users()

    users.append({
        "username": request.form["username"],
        "password": request.form["password"],
        "role": request.form["role"],
        "status": "Active",
        "last_login": "Never"
    })

    save_users(users)

    return redirect(
        url_for("user_management")
    )
@app.route("/view-user/<username>")
def view_user(username):

    users = load_users()

    for user in users:

        if user["username"] == username:

            return render_template(
                "dashboard/view_user.html",
                user=user
            )

    return redirect(
        url_for("user_management")
    )


@app.route("/toggle-user/<username>")
def toggle_user(username):

    users = load_users()

    for user in users:

        if user["username"] == username:

            if user["status"] == "Active":
                user["status"] = "Disabled"
            else:
                user["status"] = "Active"

    save_users(users)

    return redirect(
        url_for("user_management")
    )


@app.route("/delete-user/<username>")
def delete_user(username):

    users = load_users()

    users = [
        user for user in users
        if user["username"] != username
    ]

    save_users(users)

    return redirect(
        url_for("user_management")
    )


@app.route("/change-password/<username>")
def change_password_page(username):

    return render_template(
        "dashboard/change_password.html",
        username=username
    )
# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "project": PROJECT_NAME,
        "version": APP["environment"],
    }
@app.route("/soc-terminal")
def soc_terminal():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/soc_terminal.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
    )
@app.route("/honeypots")
def honeypots():

    return render_template(
        "dashboard/honeypots.html",
        username="admin",
        role="Administrator"
    )
@app.route("/api/honeypots")
def api_honeypots():

    with open(
        "data/honeypots.json",
        "r"
    ) as f:

        return json.load(f)
# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    app.run(
        host=APP["host"],
        port=APP["port"],
        debug=APP["debug"],
    )