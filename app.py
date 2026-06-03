from pathlib import Path
from collections import Counter
from datetime import timedelta, datetime

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
] = timedelta(hours=4)

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

        users = load_users()

        user = users.get(
            username
        )

        if (
            user
            and user.get(
                "active",
                True
            )
            and user.get(
                "password"
            ) == password
        ):

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
                        user["role"]
                }
            )

            flash(
                "Login successful",
                "success"
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        log_event(
            actor=username,
            action="LOGIN_FAILED"
        )

        flash(
            "Invalid credentials",
            "danger"
        )

    return render_template(
        "login.html",
        last_login="Unknown",
        active_sessions=0
    )


@app.route("/logout")
@login_required
def logout():

    log_event(
        actor=current_user(),
        action="LOGOUT"
    )

    session.clear()

    flash(
        "Logged out successfully",
        "info"
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
        role=current_role(),
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

    return render_soc_page(
        "contact.html"
    )

# ==================================================
# SOC MODULES
# ==================================================

@app.route("/alerts")
@login_required
def alerts():

    return render_soc_page(
        "alerts.html"
    )


@app.route("/attack-logs")
@login_required
def attack_logs():

    stats = get_attack_data()

    return render_template(
        "attack_logs.html",
        attacks=stats[
            "recent_attacks"
        ]
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

@app.route("/ioc-extraction")
@permission_required(
    "ioc_extraction"
)
def ioc_extraction():

    return render_template(
        "ioc_extraction.html",
        iocs=[]
    )


@app.route("/malware-analysis")
@permission_required(
    "malware_analysis"
)
def malware_analysis():

    return render_template(
        "malware_analysis.html",
        files=[]
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

    return render_soc_page(
        "ip_intelligence.html"
    )


@app.route("/asset-inventory")
@login_required
def asset_inventory():

    return render_template(
        "asset_inventory.html",
        assets=[]
    )

# ==================================================
# ADMIN MODULES
# ==================================================

@app.route("/settings")
@permission_required(
    "settings"
)
def settings():

    return render_soc_page(
        "settings.html"
    )


@app.route(
    "/user-management",
    methods=["GET", "POST"]
)
@permission_required("user_management")
def user_management():

    if request.method == "POST":
        # create/update user

        flash(
            "User saved",
            "success"
        )

    users = load_users()

    return render_template(
        "user_management.html",
        users=users
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