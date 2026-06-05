from pathlib import Path
from collections import Counter
from datetime import timedelta, datetime
import psutil
import json
import logging
import os
import uuid
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

from core.auth import (
    current_user,
    current_role,
    is_authenticated,
    login_required,
)

from core.storage import (
    ensure_data_files,
    load_users,
    save_users,
)

from core.audit import (
    log_event,
)

from core.permissions import (
    permission_required,
    has_permission,
)

# ==================================================
# APP CONFIG
# ==================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "soc-dashboard-secret"
)

app.config[
    "PERMANENT_SESSION_LIFETIME"
] = timedelta(minutes=5)

from core.permissions import (
    permission_required,
    has_permission,
)

app.jinja_env.globals[
    "has_permission"
] = has_permission

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "soc-dashboard-secret"
)

app.config[
    "PERMANENT_SESSION_LIFETIME"
] = timedelta(minutes=5)

BASE_DIR = Path(
    __file__
).resolve().parent

LOG_FILE = (
    BASE_DIR /
    "logs" /
    "cowrie.json"
)

# ==================================================
# DEFAULTS
# ==================================================

DEFAULT_STATS = {
    "total_attacks": 0,
    "unique_ips": 0,
    "recent_attacks": [],
    "country_stats": [],
    "threat_level": "LOW",
}

# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(
    __name__
)

# ==================================================
# CONTEXT PROCESSORS
# ==================================================

@app.context_processor
def inject_globals():

    return {

        "current_user":
            current_user(),

        "current_role":
            current_role(),

        "has_permission":
            has_permission,

        "year":
            datetime.now().year,

        "active_alerts":
            0,
    }

# ==================================================
# HELPERS
# ==================================================

def render_soc_page(
    template_name: str,
    **kwargs
):

    return render_template(
        template_name,
        **kwargs
    )


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


def parse_attack_record(
    data: dict
) -> dict:

    return {

        "ip":
            data.get(
                "src_ip",
                "Unknown"
            ),

        "username":
            data.get(
                "username",
                "N/A"
            ),

        "password":
            data.get(
                "password",
                "N/A"
            ),

        "timestamp":
            data.get(
                "timestamp",
                "N/A"
            ),

        "country":
            data.get(
                "country",
                "Unknown"
            ),
    }


def get_attack_data():

    attacks = []

    unique_ips = set()

    country_counter = Counter()

    if not LOG_FILE.exists():

        logger.warning(
            "Missing Cowrie log file"
        )

        return DEFAULT_STATS.copy()

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:

                    data = json.loads(
                        line
                    )

                except json.JSONDecodeError:

                    continue

                attack = (
                    parse_attack_record(
                        data
                    )
                )

                attacks.append(
                    attack
                )

                unique_ips.add(
                    attack["ip"]
                )

                country_counter[
                    attack["country"]
                ] += 1

    except Exception:

        logger.exception(
            "Failed reading logs"
        )

        return DEFAULT_STATS.copy()

    total_attacks = len(
        attacks
    )

    return {

        "total_attacks":
            total_attacks,

        "unique_ips":
            len(unique_ips),

        "recent_attacks":
            attacks[-20:][::-1],

        "country_stats":
            [
                {
                    "country": country,
                    "count": count,
                }
                for country, count
                in country_counter.most_common(
                    10
                )
            ],

        "threat_level":
            calculate_threat_level(
                total_attacks
            ),
    }


def build_error_context(
    code: str,
    title: str,
    message: str,
    description: str
):

    return {

        "error_code":
            code,

        "error_title":
            title,

        "error_message":
            message,

        "error_description":
            description,

        "error_id":
            str(
                uuid.uuid4()
            )[:8],

        "error_timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
    }

# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    stats = get_attack_data()

    return render_template(
        "home.html",
        total_attacks=stats[
            "total_attacks"
        ],
        unique_ips=stats[
            "unique_ips"
        ],
        active_alerts=0,
        threat_level=stats[
            "threat_level"
        ],
        recent_attacks=stats[
            "recent_attacks"
        ],
    )

# ==================================================
# LOGIN
# ==================================================

@app.route(
    "/login",
    methods=[
        "GET",
        "POST",
    ]
)
def login():

    if is_authenticated():

        return redirect(
            url_for(
                "dashboard"
            )
        )

    users = load_users()

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

        mfa_code = (
            request.form.get(
                "mfa_code",
                ""
            ).strip()
        )

        user = users.get(
            username
        )

        if not user:

            return render_template(
                "login.html",
                error="User not found",
                last_login="Unknown",
                active_sessions=0,
                mfa_users=[
                    name
                    for name, data
                    in users.items()
                    if data.get(
                        "mfa",
                        False
                    )
                ]
            )

        if not user.get(
            "active",
            True
        ):

            return render_template(
                "login.html",
                error="Account disabled",
                last_login="Unknown",
                active_sessions=0,
                mfa_users=[
                    name
                    for name, data
                    in users.items()
                    if data.get(
                        "mfa",
                        False
                    )
                ]
            )

        if user.get(
            "password"
        ) != password:

            log_event(
                actor=username,
                action="LOGIN_FAILED"
            )

            return render_template(
                "login.html",
                error="Invalid credentials",
                last_login="Unknown",
                active_sessions=0,
                mfa_users=[
                    name
                    for name, data
                    in users.items()
                    if data.get(
                        "mfa",
                        False
                    )
                ]
            )

        if user.get(
            "mfa",
            False
        ):

            if mfa_code != "123456":

                log_event(
                    actor=username,
                    action="MFA_FAILED"
                )

                return render_template(
                    "login.html",
                    error="Invalid MFA Code",
                    last_login="Unknown",
                    active_sessions=0,
                    mfa_users=[
                        name
                        for name, data
                        in users.items()
                        if data.get(
                            "mfa",
                            False
                        )
                    ]
                )

        session.clear()

        session[
            "user"
        ] = username

        session[
            "role"
        ] = user[
            "role"
        ]

        session.permanent = True

        log_event(
            actor=username,
            action="LOGIN_SUCCESS",
            details={
                "role":
                    user[
                        "role"
                    ]
            }
        )

        return redirect(
            url_for(
                "dashboard"
            )
        )

    return render_template(
        "login.html",
        error=None,
        last_login="Unknown",
        active_sessions=0,
        mfa_users=[
            name
            for name, data
            in users.items()
            if data.get(
                "mfa",
                False
            )
        ]
    )
@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )
# ==================================================
# DASHBOARD
# ==================================================
@app.route("/dashboard")
@login_required
def dashboard():

    stats = get_attack_data()

    cpu_usage = psutil.cpu_percent(interval=0.1)

    memory_usage = (
        psutil
        .virtual_memory()
        .percent
    )

    disk_usage = (
        psutil
        .disk_usage("C:\\")
        .percent
    )

    return render_template(
        "dashboard.html",

        total_attacks=stats.get(
            "total_attacks",
            0
        ),

        unique_ips=stats.get(
            "unique_ips",
            0
        ),

        recent_attacks=stats.get(
            "recent_attacks",
            []
        ),

        country_stats=stats.get(
            "country_stats",
            []
        ),

        threat_level=stats.get(
            "threat_level",
            "LOW"
        ),

        current_user=session.get(
            "user",
            "Unknown"
        ),

        current_role=session.get(
            "role",
            "user"
        ),

        cpu_usage=cpu_usage,

        memory_usage=memory_usage,

        disk_usage=disk_usage,

        top_attackers=[],

        audit_events=[],

        ioc_count=0,

        domain_count=0,

        hash_count=0,

        url_count=0,

        open_hunts=0,

        ioc_matches=0,

        investigations=0,

        malware_count=0
    )

# ==================================================
# INFORMATION
# ==================================================

@app.route("/about")
@login_required
def about():

    return render_soc_page(
        "about.html"
    )


@app.route("/help")
@login_required
def help():

    return render_soc_page(
        "help.html"
    )


@app.route("/contact")
@login_required
def contact():

    return redirect(
        url_for("dashboard")
    )

# ==================================================
# SOC MODULES
# ==================================================

@app.route("/alerts")
@login_required
def alerts():

    alert_stats = {
        "critical": 2,
        "high": 5,
        "medium": 12,
        "low": 18
    }

    alerts = [
        {
            "id": "ALT-001",
            "title": "SSH Brute Force Detected",
            "severity": "High",
            "source": "Cowrie",
            "status": "Open",
            "owner": "SOC Analyst",
            "timestamp": "2026-06-04 03:45"
        },
        {
            "id": "ALT-002",
            "title": "Telnet Scan Detected",
            "severity": "Medium",
            "source": "Cowrie",
            "status": "Investigating",
            "owner": "SOC Analyst",
            "timestamp": "2026-06-04 03:47"
        }
    ]

    alert_timeline = [
        {
            "timestamp": "03:45",
            "message": "SSH Brute Force Alert Generated"
        },
        {
            "timestamp": "03:47",
            "message": "Telnet Scan Alert Generated"
        }
    ]

    return render_template(
        "alerts.html",
        alert_stats=alert_stats,
        alerts=alerts,
        alert_timeline=alert_timeline
    )

@app.route("/attack-logs")
@login_required
def attack_logs():

    data = get_attack_data()

    return render_template(
        "attack_logs.html",
        recent_attacks=data.get(
            "recent_attacks",
            []
        )
    )

@app.route("/attack-statistics")
@login_required
def attack_statistics():

    stats = get_attack_data()

    return render_template(
        "attack_statistics.html",
        total_attacks=stats[
            "total_attacks"
        ],
        unique_ips=stats[
            "unique_ips"
        ],
        country_stats=stats[
            "country_stats"
        ],
    )


@app.route("/attack-timeline")
@login_required
def attack_timeline():

    stats = get_attack_data()

    return render_template(
        "attack_timeline.html",
        attacks=stats[
            "recent_attacks"
        ]
    )


@app.route("/geolocation")
@login_required
def geolocation():

    stats = get_attack_data()

    return render_template(
        "geolocation.html",
        country_stats=stats[
            "country_stats"
        ]
    )


@app.route("/reports")
@login_required
def reports():

    return render_soc_page(
        "reports.html"
    )


@app.route("/status")
@login_required
def status():

    stats = get_attack_data()

    return render_template(
        "status.html",
        stats=stats
    )

# ==================================================
# ANALYST + ADMIN
# ==================================================

@app.route("/ioc-extraction", methods=["GET", "POST"])
@login_required
def ioc_extraction():

    ioc_summary = {
        "ips": 2,
        "domains": 2,
        "urls": 1,
        "hashes": 1
    }

    iocs = [
        {
            "type": "IP",
            "value": "185.44.22.10"
        },
        {
            "type": "Domain",
            "value": "malicious-site.com"
        },
        {
            "type": "URL",
            "value": "http://bad-site.com/payload"
        },
        {
            "type": "Hash",
            "value": "44d88612fea8a8f36de82e1278abb02f"
        }
    ]

    ips = [
        "185.44.22.10",
        "91.22.15.90"
    ]

    domains = [
        "malicious-site.com",
        "evil-domain.net"
    ]

    return render_template(
        "ioc_extraction.html",
        ioc_summary=ioc_summary,
        iocs=iocs,
        ips=ips,
        domains=domains
    )

@app.route("/malware-analysis", methods=["GET", "POST"])
@login_required
def malware_analysis():

    analysis = {
        "md5":
            "44d88612fea8a8f36de82e1278abb02f",

        "sha1":
            "3395856ce81f2b7382dee72602f798b642f14140",

        "sha256":
            "275a021bbfb6488ad9f6f6c0c1f3f4b7c4e4b9e0",

        "filename":
            "suspicious.exe",

        "size":
            "2.4 MB",

        "filetype":
            "PE32 Executable",

        "score":
            87,

        "iocs": [
            "185.44.22.10",
            "malicious-site.com",
            "http://bad-site.com/payload"
        ],

        "mitre": [
            {
                "name":
                    "Command and Scripting Interpreter",
                "id":
                    "T1059"
            },
            {
                "name":
                    "Ingress Tool Transfer",
                "id":
                    "T1105"
            }
        ]
    }

    return render_template(
        "malware_analysis.html",
        analysis=analysis
    )


@app.route("/mitre-mapping")
@permission_required(
    "mitre_mapping"
)
def mitre_mapping():

    return render_template(
        "mitre_mapping.html",
        mitre_mappings=[],
        mitre_stats={}
    )


@app.route("/threat-classification")
@permission_required(
    "threat_classification"
)
def threat_classification():

    return render_template(
        "threat_classification.html",
        threats=[],
        threat_stats={}
    )


@app.route("/threat-hunting")
@permission_required(
    "threat_hunting"
)
def threat_hunting():

    return render_template(
        "threat_hunting.html",
        results=[]
    )


@app.route("/case-management")
@permission_required(
    "case_management"
)
def case_management():

    return render_template(
        "case_management.html",
        cases=[]
    )
@app.route(
    "/api/verify-mfa",
    methods=["POST"]
)
def verify_mfa():

    data = request.get_json()

    code = data.get("code")

    if code == "123456":

        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False
    }), 401

@app.route("/incident-response")
@permission_required(
    "incident_response"
)
def incident_response():

    return render_template(
        "incident_response.html",
        incidents={},
        incident_list=[]
    )

# ==================================================
# ALL USERS
# ==================================================

@app.route("/ip-intelligence")
@login_required

def ip_intelligence():

    ip = request.args.get(
        "ip",
        "8.8.8.8"
    )

    ip_info = {
        "ip": ip,
        "country": "United States",
        "city": "Mountain View",
        "isp": "Google LLC",
        "asn": "AS15169",
        "org": "Google"
    }

    whois_data = f"""
IP Address: {ip}
Country: United States
ISP: Google LLC
ASN: AS15169
"""

    return render_template(
        "ip_intelligence.html",
        ip_info=ip_info,
        whois_data=whois_data
    )


@app.route("/asset-inventory")
@login_required
def asset_inventory():

    asset_stats = {
        "total": 128,
        "online": 117,
        "critical": 12,
        "vulnerabilities": 34
    }

    assets = [
        {
            "hostname": "MRI-SERVER-01",
            "ip": "192.168.1.20",
            "type": "Server",
            "os": "Windows Server 2022",
            "owner": "Radiology",
            "status": "online",
            "risk": "Critical",
            "last_seen": "2026-06-04 03:45"
        },
        {
            "hostname": "COWRIE-HONEYPOT",
            "ip": "192.168.1.250",
            "type": "Honeypot",
            "os": "Ubuntu",
            "owner": "SOC Team",
            "status": "online",
            "risk": "High",
            "last_seen": "2026-06-04 03:47"
        }
    ]

    categories = {
        "servers": 28,
        "workstations": 54,
        "firewalls": 6,
        "network": 18,
        "iot": 20,
        "honeypots": 2
    }

    vulnerabilities = {
        "critical": 4,
        "high": 11,
        "medium": 14,
        "low": 5
    }

    return render_template(
        "asset_inventory.html",
        asset_stats=asset_stats,
        assets=assets,
        categories=categories,
        vulnerabilities=vulnerabilities
    )

# ==================================================
# ADMIN MODULES
# ==================================================

@app.route("/settings")
@permission_required("settings")
def settings():

    return render_soc_page(
        "settings.html"
    )


# ==================================================
# USER MANAGEMENT
# ==================================================

@app.route(
    "/user-management",
    methods=["GET", "POST"]
)
@permission_required("user_management")
def user_management():

    users = load_users()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")

        if username and password:

           users[username] = {
    "password": password,
    "role": role,
    "active": True,
    "mfa": request.form.get("mfa") == "on",
    "last_login": "Never",
    "force_password_change": True
}

            save_users(users)

            flash(
                "User created successfully",
                "success"
            )

            return redirect(
                url_for("user_management")
            )

    return render_template(
        "user_management.html",
        users=users
    )


# ==================================================
# EDIT USER
# ==================================================

@app.route(
    "/user-management/edit/<username>",
    methods=["GET", "POST"]
)
@permission_required("user_management")
def edit_soc_user(username):

    users = load_users()

    if username not in users:

        flash(
            "User not found",
            "danger"
        )

        return redirect(
            url_for("user_management")
        )

    if request.method == "POST":

        new_username = request.form.get(
            "username"
        )

        role = request.form.get(
            "role"
        )

        active = (
            request.form.get("active")
            == "on"
        )

        mfa = (
            request.form.get("mfa")
            == "on"
        )

        user_data = users.pop(
            username
        )

        user_data["role"] = role
        user_data["active"] = active
        user_data["mfa"] = mfa

        users[new_username] = user_data

        save_users(users)

        flash(
            "User updated successfully",
            "success"
        )

        return redirect(
            url_for("user_management")
        )

    return render_template(
        "edit_user.html",
        username=username,
        user=users[username]
    )


# ==================================================
# DELETE USER
# ==================================================

@app.route(
    "/user-management/delete/<username>"
)
@permission_required("user_management")
def delete_user(username):

    users = load_users()

    if username in users:

        users.pop(username)

        save_users(users)

        flash(
            f"{username} deleted successfully",
            "success"
        )

    return redirect(
        url_for("user_management")
    )


# ==================================================
# TOGGLE MFA
# ==================================================

@app.route(
    "/user-management/mfa/<username>"
)
@permission_required("user_management")
def toggle_mfa(username):

    users = load_users()

    if username in users:

        users[username]["mfa"] = not users[
            username
        ].get(
            "mfa",
            False
        )

        save_users(users)

        flash(
            "MFA Updated",
            "success"
        )

    return redirect(
        url_for("user_management")
    )


# ==================================================
# RESET PASSWORD
# ==================================================

@app.route(
    "/user-management/reset/<username>"
)
@permission_required("user_management")
def reset_password(username):

    users = load_users()

    if username in users:

        users[username]["password"] = "Temp123!"
        users[username]["force_password_change"] = True

        save_users(users)

        flash(
            "Password Reset",
            "success"
        )

    return redirect(
        url_for("user_management")
    )

@app.route("/audit-logs")
@permission_required(
    "audit_logs"
)
def audit_logs():

    return render_template(
        "audit_logs.html",
        audit_logs=[],
        audit_stats={}
    )

# ==================================================
# API
# ==================================================
@app.route("/api/session")
@login_required
def api_session():

    return jsonify({

        "authenticated": True,

        "user": session.get("user"),

        "role": session.get("role")

    })
@app.route("/api/alerts")
@login_required
def api_alerts():

    return jsonify({

        "count": 0,

        "alerts": []

    })

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
@app.route("/api/user-role/<username>")
@login_required
def api_user_role(username):

    users = load_users()

    user = users.get(username)

    if not user:

        return jsonify({
            "success": False,
            "role": None
        })

    return jsonify({
        "success": True,
        "role": user.get("role", "user")
    })

@app.route("/api/health")
def api_health():

    return jsonify(
        {
            "status":
                "healthy",
            "service":
                "soc-dashboard",
            "version":
                "2.0"
        }
    )

# ==================================================
# DEBUG ROUTES
# ==================================================

@app.route("/debug-session")
@login_required
def debug_session():

    return jsonify(
        {
            "user":
                session.get(
                    "user"
                ),

            "role":
                session.get(
                    "role"
                ),

            "session":
                dict(
                    session
                ),
        }
    )


@app.route("/debug-role")
@login_required
def debug_role():

    return jsonify(
        {
            "user":
                session.get(
                    "user"
                ),

            "role":
                session.get(
                    "role"
                ),
        }
    )


@app.route("/debug-permissions")
@login_required
def debug_permissions():

    from core.storage import (
        load_permissions
    )

    return jsonify(
        load_permissions()
    )


@app.route("/routes")
def routes():

    return jsonify(
        {
            "routes":
                sorted(
                    [
                        str(rule)
                        for rule in
                        app.url_map.iter_rules()
                    ]
                )
        }
    )

# ==================================================
# ERROR HANDLERS
# ==================================================

@app.errorhandler(401)
def unauthorized(error):

    return (
        render_template(
            "error.html",
            **build_error_context(
                "401",
                "Unauthorized",
                "LOGIN REQUIRED",
                "Authentication required."
            )
        ),
        401,
    )


@app.errorhandler(403)
def forbidden(error):

    return (
        render_template(
            "error.html",
            **build_error_context(
                "403",
                "Forbidden",
                "ACCESS DENIED",
                "Permission denied."
            )
        ),
        403,
    )


@app.errorhandler(404)
def not_found(error):

    return (
        render_template(
            "error.html",
            **build_error_context(
                "404",
                "Page Not Found",
                "NOT FOUND",
                "The requested page does not exist."
            )
        ),
        404,
    )


@app.errorhandler(500)
def server_error(error):

    logger.exception(
        "Unhandled server error"
    )

    return (
        render_template(
            "error.html",
            **build_error_context(
                "500",
                "Server Error",
                "SERVER ERROR",
                "Unexpected application error."
            )
        ),
        500,
    )

# ==================================================
# STARTUP
# ==================================================

def startup():

    ensure_data_files()

    logger.info(
        "SOC Dashboard Started"
    )

    logger.info(
        "Cowrie Log File: %s",
        LOG_FILE
    )


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    startup()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )