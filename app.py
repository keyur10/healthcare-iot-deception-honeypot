from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from core.config import APP
from ipwhois import IPWhois

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

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/dashboard.html",
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME,
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

# ==================================================
# IOC EXTRACTION
# ==================================================

@app.route("/ioc")
def ioc():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/ioc.html",
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


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    app.run(
        host=APP["host"],
        port=APP["port"],
        debug=APP["debug"],
    )