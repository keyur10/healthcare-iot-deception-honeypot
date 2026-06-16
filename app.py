# ==================================================
# IMPORTS
# ==================================================
from __future__ import annotations

# 1. Standard Library
import os
import json
import shutil
import csv
import tempfile
import ipaddress
from datetime import datetime
from typing import Any

# 2. Third-Party
import requests
from flask import (
    Flask, flash, redirect, render_template, 
    request, url_for, session, make_response, send_file
)
from reportlab.pdfgen import canvas
from ipwhois import IPWhois

try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

# 3. Local Core Modules
from core.storage import (
    ensure_data_files, load_users, save_users,
    load_attacks, save_attacks, load_honeypots,
    save_honeypots, load_settings, save_settings,
    load_audit_logs, save_audit_logs
)
from core.config import APP, SECRET_KEY, PROJECT_NAME
from core.helpers import configure_logging
from core.audit import log_event
from core.auth import (
    login_user, logout_user, is_authenticated,
    current_user, current_role, has_permission, get_all_users
)
from core.attack_manager import create_attack

# ==================================================
# UTILITIES & CONSTANTS
# ==================================================
DEVICES_FILE = "data/devices.json"

def load_devices():
    if not os.path.exists(DEVICES_FILE):
        return []
    with open(DEVICES_FILE, "r") as file:
        return json.load(file)

def save_devices(devices):
    with open(DEVICES_FILE, "w") as file:
        json.dump(devices, file, indent=4)

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

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
        severity="INFO",
        message="Application started",
    )

initialize_app()

# ==================================================
# HELPERS
# ==================================================

def get_current_permissions() -> dict:

    users = load_users()

    username = current_user()

    for user in users:

        if (
            isinstance(user, dict)
            and
            user.get("username") == username
        ):

            return user.get(
                "permissions",
                {}
            )

    return {}


def hunt_threats() -> list:

    return []

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
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        if login_user(
            username,
            password
        ):

            flash(
                "Login successful",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid credentials",
            "danger"
        )

    return render_template(
        "auth/login.html",
        project_name=PROJECT_NAME
    )

# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    logout_user()

    flash(
        "Logged out successfully",
        "info"
    )

    return redirect(
        url_for("login")
    )

# ==================================================
# HEALTH
# ==================================================

@app.route("/health")
def health():

    return {

        "status": "ok",

        "project": PROJECT_NAME,

        "environment": APP["environment"]

    }
# ==================================================
# DASHBOARD
# ==================================================

@app.route("/dashboard")
def dashboard():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    attacks = load_attacks()

    honeypots = load_honeypots()

    users = load_users()

    active_honeypots = len([

        hp

        for hp in honeypots

        if hp.get("status") == "Running"

    ])

    total_attacks = len(
        attacks
    )

    total_users = len(
        users
    )

    critical_attacks = len([

        attack

        for attack in attacks

        if attack.get("risk") == "Critical"

    ])

    return render_template(
        "dashboard/dashboard.html",

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME,

        active_honeypots=active_honeypots,

        total_attacks=total_attacks,

        total_users=total_users,

        critical_attacks=critical_attacks,

        attacks=attacks[-10:]
    )
@app.route("/threat-hunting")
def threat_hunting():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    attacks = load_attacks()

    hunt_results = []

    for attack in attacks:

        hunt_results.append({

            "time":
                attack.get(
                    "time",
                    "N/A"
                ),

            "source_ip":
                attack.get(
                    "ip",
                    "N/A"
                ),

            "attack_type":
                attack.get(
                    "attack_type",
                    "Unknown"
                ),

            "target":
                attack.get(
                    "target",
                    "Healthcare IoT Device"
                ),

            "risk":
                attack.get(
                    "risk",
                    "Low"
                )
        })

    return render_template(

        "dashboard/threat_hunting.html",

        hunt_results=hunt_results[::-1],

        username=current_user(),

        role=current_role(),

        project_name=PROJECT_NAME
    )
@app.route(
    "/api/threat-hunt",
    methods=["POST"]
)
def threat_hunt_api():

    query = request.json.get(
        "query",
          "" ).lower()

    attacks = load_attacks()

    results = []

    for attack in attacks:

        if (

            query in str(
                attack.get("ip", "")
            ).lower()

            or

            query in str(
                attack.get(
                    "username",
                    ""
                )
            ).lower()

            or

            query in str(
                attack.get(
                    "attack_type",
                    ""
                )
            ).lower()

        ):

            results.append(
                attack
            )

    return {

        "results":
            results
    }
@app.route("/alerts")
def alerts():
    if not is_authenticated():
        return redirect(url_for("login"))

    attacks = load_attacks()
    alerts = []

    for i, attack in enumerate(attacks):
        alerts.append({
            "id": i + 1,
            "time": attack.get("time", "N/A"),
            "severity": attack.get("risk", "Low"),
            "source_ip": attack.get("ip", "N/A"),
            "target_device": attack.get("target", "Healthcare IoT Device"),
            "alert_type": attack.get("attack_type", "Unknown"),
            "status": "Open"  
        })

    # Count Severities
    critical_count = len([x for x in alerts if x["severity"] == "Critical"])
    high_count = len([x for x in alerts if x["severity"] == "High"])
    medium_count = len([x for x in alerts if x["severity"] == "Medium"])
    low_count = len([x for x in alerts if x["severity"] == "Low"])

    open_incidents_count = len(alerts)

    return render_template(
        "dashboard/alerts.html",
        alerts=alerts[::-1],  
        incidents=[],         
        threat_feed=[],
        critical_count=critical_count,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        open_incidents_count=open_incidents_count,
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME
    )
@app.route("/api/alerts")
def api_alerts():

    attacks = load_attacks()

    return {

        "alerts":
            attacks[-20:]
    }
@app.route(
    "/api/alert-action",
    methods=["POST"]
)
def alert_action():

    data = request.json

    action = data.get("action")
    target = data.get("target")

    # BLOCK IP

    if action == "block_ip":

        blocked = load_json(
            "data/blocked_ips.json"
        )

        blocked.append({

            "ip": target,

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })

        save_json(
            "data/blocked_ips.json",
            blocked
        )

        return {
            "success": True,
            "message": f"{target} blocked"
        }

    # ISOLATE DEVICE

    elif action == "isolate_device":

        devices = load_json(
            "data/isolated_devices.json"
        )

        devices.append({

            "device": target,

            "status": "Isolated"

        })

        save_json(
            "data/isolated_devices.json",
            devices
        )

        return {
            "success": True,
            "message": f"{target} isolated"
        }

    # CREATE INCIDENT

    elif action == "create_incident":

        incidents = load_json(
            "data/incidents.json"
        )

        incident_id = f"INC-{len(incidents)+1:03}"

        incidents.append({

            "id": incident_id,

            "target": target,

            "status": "Investigating",

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })

        save_json(
            "data/incidents.json",
            incidents
        )

        return {
            "success": True,
            "message": f"{incident_id} created"
        }

    # ESCALATE

    elif action == "escalate":

        return {
            "success": True,
            "message": "Escalated to SOC L2"
        }

    # RESOLVE

    elif action == "resolve":

        return {
            "success": True,
            "message": "Incident resolved"
        }

    return {
        "success": False
    }
@app.route("/timeline")
def timeline():

    attacks = load_attacks()

    critical_events = len([

        attack

        for attack in attacks

        if attack.get("risk") == "Critical"

    ])

    return render_template(

        "dashboard/timeline.html",

        attacks=attacks,

        critical_events=critical_events,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME

    )
@app.route("/geolocation")
def geolocation():

    attacks = load_attacks()

    return render_template(
        "dashboard/geolocation.html",

        attacks=attacks,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
# ==================================================
# IOC 
# ==================================================
@app.route("/ioc")
def ioc():

    attacks = load_attacks()

    iocs = []

    for attack in attacks:

        if attack.get("ip"):

            iocs.append({

                "ioc_type":
                    "IP Address",

                "value":
                    attack.get("ip"),

                "risk":
                    attack.get("risk", "High"),

                "source":
                    "Network Traffic",

                "time":
                    attack.get("time", "N/A")
            })

        if attack.get("username"):

            iocs.append({

                "ioc_type":
                    "Username",

                "value":
                    attack.get("username"),

                "risk":
                    "Medium",

                "source":
                    "Credential Capture",

                "time":
                    attack.get(
                        "time",
                        "N/A"
                    )
            })

    return render_template(

        "dashboard/ioc.html",

        iocs=iocs,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
@app.route("/export-ioc")
def export_ioc():

    attacks = load_attacks()

    iocs = []

    for attack in attacks:

        if attack.get("ip"):

            iocs.append({

                "ioc_type":
                    "IP Address",

                "value":
                    attack.get("ip"),

                "risk":
                    attack.get(
                        "risk",
                        "Low"
                    ),

                "source":
                    attack.get(
                        "attack_type",
                        "Honeypot"
                    ),

                "time":
                    attack.get(
                        "time",
                        "N/A"
                    )
            })

    export_file = "ioc_report.json"

    with open(
        export_file,
        "w"
    ) as f:

        json.dump(
            iocs,
            f,
            indent=4
        )

    return send_file(

        export_file,

        as_attachment=True,

        download_name=
            "ioc_report.json"
    )
@app.route("/whois", methods=["POST"])
def whois_lookup():

    ip = request.form.get(
        "ip",
        ""
    ).strip()

    try:

        ip_obj = ipaddress.ip_address(ip)

        if (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_reserved
            or ip_obj.is_multicast
        ):

            flash(
                "Private/Internal IP addresses cannot be queried with WHOIS. Please enter a public IP address.",
                "danger"
            )

            return redirect(
                url_for("dashboard")
            )

        obj = IPWhois(ip)

        result = obj.lookup_rdap()

        session["whois_result"] = {

            "ip": ip,

            "country":
                result.get(
                    "asn_country_code",
                    "Unknown"
                ),

            "asn":
                result.get(
                    "asn",
                    "Unknown"
                ),

            "provider":
                result.get(
                    "asn_description",
                    "Unknown"
                )

        }

        flash(
            "WHOIS Lookup Successful",
            "success"
        )

    except ValueError:

        flash(
            "Invalid IP Address Format",
            "danger"
        )

    except Exception as e:

        print(
            "WHOIS ERROR:",
            e
        )

        flash(
            f"Lookup Failed: {e}",
            "danger"
        )

    return redirect(
        url_for("dashboard")
    )

@app.route("/honeypots")
def honeypots():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    honeypot_list = load_honeypots()

    attacks = load_attacks()

    running_count = len([

        hp

        for hp in honeypot_list

        if hp.get("status") == "Running"

    ])

    stopped_count = len(
        honeypot_list
    ) - running_count

    return render_template(
        "dashboard/honeypots.html",

        honeypots=honeypot_list,

        running_count=running_count,

        stopped_count=stopped_count,

        total_attacks=len(attacks),

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
@app.route(
    "/add-honeypot",
    methods=["POST"]
)
def add_honeypot():

    honeypots = load_honeypots()

    new_id = 1

    if honeypots:

        new_id = max(
            hp.get("id", 0)
            for hp in honeypots
        ) + 1

    honeypots.append({

        "id": new_id,

        "name":
            request.form.get(
                "name"
            ),

        "type":
            request.form.get(
                "type"
            ),

        "ip":
            request.form.get(
                "ip"
            ),

        "port":
            int(
                request.form.get(
                    "port",
                    0
                )
            ),

        "status":
            "Stopped",

        "attacks":
            0
    })

    save_honeypots(
        honeypots
    )

    flash(
        "Honeypot Created",
        "success"
    )

    return redirect(
        url_for("honeypots")
    )
@app.route(
    "/view-honeypot/<int:hp_id>"
)
def view_honeypot(hp_id):

    honeypots = load_honeypots()

    for hp in honeypots:

        if hp.get("id") == hp_id:

            return render_template(
                "dashboard/view_honeypot.html",

                hp=hp,

                username=current_user(),

                role=current_role(),

                permissions=get_current_permissions(),

                project_name=PROJECT_NAME
            )

    flash(
        "Honeypot Not Found",
        "danger"
    )

    return redirect(
        url_for("honeypots")
    )
@app.route(
    "/start-honeypot/<int:hp_id>"
)
def start_honeypot(hp_id):

    honeypots = load_honeypots()

    for hp in honeypots:

        if hp.get("id") == hp_id:

            hp["status"] = "Running"

            break

    save_honeypots(
        honeypots
    )

    flash(
        "Honeypot Started",
        "success"
    )

    return redirect(
        url_for("honeypots")
    )
@app.route(
    "/stop-honeypot/<int:hp_id>"
)
def stop_honeypot(hp_id):

    honeypots = load_honeypots()

    for hp in honeypots:

        if hp.get("id") == hp_id:

            hp["status"] = "Stopped"

            break

    save_honeypots(
        honeypots
    )

    flash(
        "Honeypot Stopped",
        "warning"
    )

    return redirect(
        url_for("honeypots")
    )
@app.route(
    "/delete-honeypot/<int:hp_id>"
)
def delete_honeypot(hp_id):

    honeypots = load_honeypots()

    honeypots = [

        hp

        for hp in honeypots

        if hp.get("id") != hp_id

    ]

    save_honeypots(
        honeypots
    )

    flash(
        "Honeypot Deleted",
        "success"
    )

    return redirect(
        url_for("honeypots")
    )
@app.route("/devices")
def devices():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    devices = load_devices()

    online_count = len([

        device

        for device in devices

        if device.get("status") == "Online"

    ])

    offline_count = len(
        devices
    ) - online_count

    return render_template(

        "dashboard/devices.html",

        devices=devices,

        total_devices=len(devices),

        online_count=online_count,

        offline_count=offline_count,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME

    )
@app.route(
    "/add-device",
    methods=["POST"]
)
def add_device():

    devices = load_devices()

    new_id = 1

    if devices:

        new_id = max(

            d.get(
                "id",
                0
            )

            for d in devices

        ) + 1

    devices.append({

        "id": new_id,

        "name":
            request.form.get(
                "name"
            ),

        "type":
            request.form.get(
                "type"
            ),

        "ip":
            request.form.get(
                "ip"
            ),

        "status":
            "Online",

        "risk":
            "Low",

        "last_seen":
            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    })

    save_devices(
        devices
    )


@app.route(
    "/delete-device/<int:device_id>"
)
def delete_device(
    device_id
):

    devices = [

        d

        for d in load_devices()

        if d.get("id")
        != device_id

    ]

    save_devices(
        devices
    )

    flash(
        "Device Removed",
        "success"
    )

    return redirect(
        url_for("devices")
    )


# ==================================================
# DASHBOARD API STATS
# ==================================================

@app.route("/api/stats")
def api_stats():
    if not is_authenticated():
        return {"error": "Unauthorized"}, 401
    attacks = load_attacks()

    stats = {
        "active_honeypots": 24,
        "live_attacks": len(attacks),
        "ioc_count": 309,
        "devices": 98,
        "mitre": 37,
        "critical": 5,
        "high": 12,
        "medium": 18,
        "low": 26
    }

    return stats


# ==================================================
# MITRE API
# ==================================================
@app.route("/mitre")
def mitre_page():
    # 1. Security Check
    if not is_authenticated():
        return redirect(url_for("login"))

    # 2. Load the real attack data from your JSON file
    attacks = load_attacks()

    # 3. Setup counters for the HTML to use
    risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    tactics = {"initial_access": 0, "discovery": 0, "execution": 0, "persistence": 0}
    mitre_data = []

    # 4. Analyze the attacks and do the math
    for attack in attacks:
        # Tally the risks
        severity = attack.get("severity", "Low")
        if severity in risk_counts:
            risk_counts[severity] += 1
        else:
            risk_counts["Low"] += 1

        # Logic to map Honeypot attacks to MITRE Tactics
        port = str(attack.get("port", ""))
        technique = "T1190" # Default Fallback
        
        if port in ["22", "2222"]: # SSH Brute Force
            tactics["initial_access"] += 1
            technique = "T1110 (Brute Force)"
        elif port in ["80", "443", "8080"]: # Web exploits
            tactics["execution"] += 1
            technique = "T1190 (Exploit Public App)"
        else: # Other scans
            tactics["discovery"] += 1
            technique = "T1046 (Network Service Discovery)"

        # Format the data for the frontend table
        mitre_data.append({
            "time": attack.get("timestamp", "Unknown"),
            "source_ip": attack.get("ip", attack.get("source_ip", "Unknown")),
            "technique": technique,
            "target": attack.get("honeypot", "Unknown Node"),
            "risk": severity
        })

    # 5. Pass EVERYTHING to the HTML (Notice how this is outside the loop!)
    return render_template(
        "dashboard/mitre.html",
        mitre_data=mitre_data,
        risk_counts=risk_counts,
        initial_access=tactics["initial_access"],
        discovery=tactics["discovery"],
        execution=tactics["execution"],
        persistence=tactics["persistence"],
        username=current_user(),
        role=current_role(),
        project_name=PROJECT_NAME
    )

#================================================== 
# SETTINGS
# ==================================================
@app.route("/settings")
def settings():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    settings_data = load_settings()

    users = load_users()

    return render_template(
        "dashboard/settings.html",

        settings=settings_data,

        users=users,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
@app.route("/settings/user-management")
def user_management():

    if current_role() != "Administrator":

        flash(
            "Access Denied",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    users = load_users()

    total_users = len(
        users
    )

    admins = sum(

        1

        for user in users

        if user.get("role")
        == "Administrator"

    )

    analysts = sum(

        1

        for user in users

        if user.get("role")
        == "Threat Analyst"

    )

    disabled_accounts = sum(

        1

        for user in users

        if user.get("status")
        == "Disabled"

    )

    return render_template(
        "dashboard/user_management.html",

        users=users,

        total_users=total_users,

        admins=admins,

        analysts=analysts,

        disabled_accounts=disabled_accounts,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
@app.route(
    "/add-user",
    methods=["POST"]
)
def add_user():

    if current_role() != "Administrator":

        return redirect(
            url_for("dashboard")
        )

    users = load_users()

    username = request.form.get(
        "username"
    )

    for user in users:

        if user.get(
            "username"
        ) == username:

            flash(
                "Username already exists",
                "danger"
            )

            return redirect(
                url_for("user_management")
            )

    users.append({

        "username":
            username,

        "password":
            request.form.get(
                "password"
            ),

        "role":
            request.form.get(
                "role"
            ),

        "status":
            "Active",

        "last_login":
            "Never",

        "permissions": {

            "dashboard": True,

            "attack_logs": False,

            "alerts": False,

            "timeline": False,

            "geolocation": False,

            "mitre": False,

            "ioc": False,

            "threat_hunting": False,

            "soc_terminal": False,

            "reports": False,

            "settings": False,

            "user_management": False
        }
    })

    save_users(
        users
    )

    flash(
        "User Created",
        "success"
    )

    return redirect(
        url_for("user_management")
    )
@app.route(
    "/view-user/<username>"
)
def view_user(username):

    users = load_users()

    user = next(

        (
            u

            for u in users

            if u.get("username")
            == username
        ),

        None

    )

    if not user:

        flash(
            "User Not Found",
            "danger"
        )

        return redirect(
            url_for("user_management")
        )

    return render_template(
        "dashboard/view_user.html",

        user=user,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
@app.route("/user-permissions/<username>")
def user_permissions(username):

    if current_role() != "Administrator":

        flash(
            "Access Denied",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    users = load_users()

    user = next(

        (
            u

            for u in users

            if u.get("username") == username

        ),

        None

    )

    if not user:

        flash(
            "User Not Found",
            "danger"
        )

        return redirect(
            url_for("user_management")
        )

    return render_template(

        "dashboard/user_permissions.html",

        user=user,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME

    )
@app.route("/change-password-page/<username>")
def change_password_page(username):

    if current_role() != "Administrator":

        flash(
            "Access Denied",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    users = load_users()

    user = next(

        (
            u

            for u in users

            if u.get("username") == username

        ),

        None

    )

    if not user:

        flash(
            "User Not Found",
            "danger"
        )

        return redirect(
            url_for("user_management")
        )

    return render_template(

        "dashboard/change_password.html",

        user=user,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME

    )
@app.route(
    "/save-permissions/<username>",
    methods=["POST"]
)
def save_permissions(username):

    if current_role() != "Administrator":

        return redirect(
            url_for("dashboard")
        )

    users = load_users()

    permissions = {

        "dashboard":
            "dashboard"
            in request.form,

        "attack_logs":
            "attack_logs"
            in request.form,

        "alerts":
            "alerts"
            in request.form,

        "timeline":
            "timeline"
            in request.form,

        "geolocation":
            "geolocation"
            in request.form,

        "mitre":
            "mitre"
            in request.form,

        "ioc":
            "ioc"
            in request.form,

        "threat_hunting":
            "threat_hunting"
            in request.form,

        "soc_terminal":
            "soc_terminal"
            in request.form,

        "reports":
            "reports"
            in request.form,

        "settings":
            "settings"
            in request.form,

        "user_management":
            "user_management"
            in request.form
    }

    for user in users:

        if user.get(
            "username"
        ) == username:

            user[
                "permissions"
            ] = permissions

            break

    save_users(
        users
    )

    flash(
        "Permissions Updated",
        "success"
    )

    return redirect(
        url_for("user_management")
    )
@app.route(
    "/toggle-user/<username>"
)
def toggle_user(username):

    if current_role() != "Administrator":

        return redirect(
            url_for("dashboard")
        )

    users = load_users()

    for user in users:

        if user.get(
            "username"
        ) == username:

            user["status"] = (

                "Disabled"

                if user.get(
                    "status"
                ) == "Active"

                else

                "Active"

            )

            break

    save_users(
        users
    )

    return redirect(
        url_for("user_management")
    )
@app.route(
    "/delete-user/<username>"
)
def delete_user(username):

    if current_role() != "Administrator":

        return redirect(
            url_for("dashboard")
        )

    if username == current_user():

        flash(
            "Cannot delete yourself",
            "danger"
        )

        return redirect(
            url_for("user_management")
        )

    users = [

        user

        for user in load_users()

        if user.get(
            "username"
        ) != username

    ]

    save_users(
        users
    )

    flash(
        "User Deleted",
        "success"
    )

    return redirect(
        url_for("user_management")
    )
@app.route(
    "/change-password/<username>",
    methods=["POST"]
)
def change_password(username):

    users = load_users()

    new_password = request.form.get(
        "password"
    )

    for user in users:

        if user.get(
            "username"
        ) == username:

            user[
                "password"
            ] = new_password

            break

    save_users(
        users
    )

    flash(
        "Password Updated",
        "success"
    )

    return redirect(
        url_for("user_management")
    )
@app.route("/save-settings", methods=["POST"])
def save_system_settings():

    flash(
        "Settings Saved Successfully",
        "success"
    )

    return redirect(
        url_for("settings")
    )

    data = {

        "security": {

            "password_length":

                request.form.get(
                    "password_length"
                ),

            "session_timeout":

                request.form.get(
                    "session_timeout"
                ),

            "two_factor":

                "two_factor"
                in request.form
        },

        "api_keys": {

            "virustotal":

                request.form.get(
                    "virustotal"
                ),

            "abuseipdb":

                request.form.get(
                    "abuseipdb"
                ),

            "shodan":

                request.form.get(
                    "shodan"
                ),

            "otx":

                request.form.get(
                    "otx"
                )
        }
    }

    save_settings(
        data
    )

    flash(
        "Settings Saved",
        "success"
    )

    return redirect(
        url_for("settings")
    )
@app.route("/create-backup")
def create_backup():

    if current_role() != "Administrator":

        return redirect(
            url_for("dashboard")
        )

    backup_name = (

        "backup_"

        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

    )

    shutil.make_archive(
        backup_name,
        "zip",
        "data"
    )

    flash(
        "Backup Created",
        "success"
    )

    return redirect(
        url_for("settings")
    )

@app.route("/reports")
def reports():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    if not has_permission(
        "reports"
    ):

        flash(
            "Access Denied",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    attacks = load_attacks()

    honeypots = load_honeypots()

    users = load_users()

    return render_template(
        "dashboard/reports.html",

        attacks=attacks,

        honeypots=honeypots,

        users=users,

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )

@app.route("/audit-logs")
def audit_logs_page():
    if not is_authenticated():
        return redirect(url_for("login"))
    
    if current_role() != "Administrator":
        flash("Access Denied: Admins Only", "danger")
        return redirect(url_for("dashboard"))

    logs = load_audit_logs()

    return render_template(
        "dashboard/audit_logs.html",
        logs=logs,
        username=current_user(),
        role=current_role(),
        permissions=get_current_permissions(),
        project_name=PROJECT_NAME
    )

@app.route("/export/csv")
def export_csv():

    attacks = load_attacks()

    response = make_response()

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=attacks.csv"

    response.headers[
        "Content-Type"
    ] = "text/csv"

    writer = csv.writer(
        response.stream
    )

    writer.writerow([
        "Time",
        "Source IP",
        "Country",
        "Attack",
        "Target",
        "Risk"
    ])

    for attack in attacks:

        writer.writerow([

            attack.get(
                "time"
            ),

            attack.get(
                "source_ip"
            ),

            attack.get(
                "country"
            ),

            attack.get(
                "attack_type"
            ),

            attack.get(
                "target"
            ),

            attack.get(
                "risk"
            )

        ])

    return response
@app.route("/export/excel")
def export_excel():

    attacks = load_attacks()

    wb = Workbook()

    ws = wb.active

    ws.title = "Attacks"

    ws.append([
        "Time",
        "Source IP",
        "Country",
        "Attack",
        "Target",
        "Risk"
    ])

    for attack in attacks:

        ws.append([

            attack.get("time"),

            attack.get("source_ip"),

            attack.get("country"),

            attack.get("attack_type"),

            attack.get("target"),

            attack.get("risk")

        ])

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    wb.save(
        temp_file.name
    )

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name="attacks.xlsx"
    )
@app.route("/export/pdf")
def export_pdf():

    attacks = load_attacks()

    pdf_file = "attack_report.pdf"

    c = canvas.Canvas(
        pdf_file
    )

    y = 800

    c.drawString(
        50,
        y,
        "Attack Report"
    )

    y -= 30

    for attack in attacks[:50]:

        c.drawString(

            50,

            y,

            f"{attack.get('source_ip')} | {attack.get('risk')}"

        )

        y -= 20

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )
@app.route("/attack-logs")
def attack_logs():
    
    attacks = load_attacks()

    total_attacks = len(attacks)
    
    critical_threats = 0
    for attack in attacks:
        
        threat_level = attack.get("severity", attack.get("risk", ""))
        
        if threat_level.strip().upper() == "CRITICAL":
            critical_threats += 1

    return render_template(
        "dashboard/attack_logs.html",
        attacks=attacks,
        total_attacks=total_attacks,
        critical_threats=critical_threats,  
        username=current_user(),
        role=current_role(),
        permissions=get_current_permissions(),
        project_name=PROJECT_NAME
    )
@app.route("/terminal")
def soc_terminal():

    if not is_authenticated():

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard/soc_terminal.html",

        username=current_user(),

        role=current_role(),

        permissions=get_current_permissions(),

        project_name=PROJECT_NAME
    )
@app.route(
    "/api/terminal",
    methods=["POST"]
)
def terminal_command():

    command = request.json.get(
        "command",
        ""
    )

    if command == "users":

        return {
            "output":
                str(
                    len(
                        load_users()
                    )
                )
        }

    if command == "attacks":

        return {
            "output":
                str(
                    len(
                        load_attacks()
                    )
                )
        }

    if command == "honeypots":

        return {
            "output":
                str(
                    len(
                        load_honeypots()
                    )
                )
        }

    if command == "status":

        return {
            "output":
                "SOC HEALTHY"
        }

    return {

        "output":
            "Unknown Command"

    }
@app.route("/api/dashboard")
def dashboard_api():

    attacks = load_attacks()
    honeypots = load_honeypots()

    unique_ips = len(
        set(
            attack.get("ip", "")
            for attack in attacks
        )
    )

    return {

        "total_attacks": len(attacks),

        "unique_ips": unique_ips,

        "threat_level": "LOW",

        "recent_attacks": attacks[-10:],

        "honeypots": len(honeypots),

        "critical": len([
            attack
            for attack in attacks
            if attack.get("risk") == "Critical"
        ])
    }
@app.route("/api/geolocate/<ip>")
def geolocate_ip(ip):

    try:

        response = requests.get(
            f"http://ip-api.com/json/{ip}"
        )

        data = response.json()

        return {

            "status": "success",

            "ip": ip,

            "country": data.get("country"),

            "city": data.get("city"),

            "region": data.get("regionName"),

            "lat": data.get("lat"),

            "lon": data.get("lon"),

            "isp": data.get("isp")

        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )