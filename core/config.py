from pathlib import Path

# ==================================================
# PROJECT
# ==================================================

PROJECT_NAME = "Healthcare IoT Deception Honeypot Network"
PROJECT_SHORT_NAME = "HIDHN"
VERSION = "2.0.0"

SECRET_KEY = "change-this-before-production"

# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"
HONEYPOT_DIR = BASE_DIR / "honeypots"
STATIC_DIR = BASE_DIR / "static"
TEMPLATE_DIR = BASE_DIR / "templates"

# ==================================================
# APP
# ==================================================

APP = {
    "environment": "development",
    "debug": True,
    "host": "0.0.0.0",
    "port": 5000,
}

# ==================================================
# SECURITY
# ==================================================

SECURITY = {
    "session_timeout_minutes": 30,
    "max_login_attempts": 5,
    "password_min_length": 8,
    "mfa_enabled": False,
    "audit_logging": True,
}

# ==================================================
# DASHBOARD
# ==================================================

DASHBOARD = {
    "auto_refresh": True,
    "refresh_interval": 10,
    "show_attack_feed": True,
    "show_threat_feed": True,
    "show_terminal": True,
    "show_mitre_panel": True,
    "show_health_panel": True,
    "show_geo_map": True,
    "show_charts": True,
}

# ==================================================
# THEME
# ==================================================

THEME = {
    "default": "soc_dark",
    "animations": True,
    "glass_effect": True,
    "medical_theme": True,
}

# ==================================================
# DEVICE PROFILES
# ==================================================

DEVICE_PROFILES = {
    "patient_monitor": {
        "vendor": "Philips",
        "model": "IntelliVue MX450",
        "port": 8080,
        "protocol": "HTTP",
    },
    "infusion_pump": {
        "vendor": "Baxter",
        "model": "Sigma Spectrum",
        "port": 8443,
        "protocol": "HTTPS",
    },
    "smart_hvac": {
        "vendor": "Johnson Controls",
        "model": "Metasys",
        "port": 47808,
        "protocol": "BACnet",
    },
    "smart_bed": {
        "vendor": "Hillrom",
        "model": "Progressa",
        "port": 9000,
        "protocol": "TCP",
    },
    "medical_imaging": {
        "vendor": "GE Healthcare",
        "model": "Revolution CT",
        "port": 104,
        "protocol": "DICOM",
    },
    "nurse_station": {
        "vendor": "Cerner",
        "model": "Care Station",
        "port": 443,
        "protocol": "HTTPS",
    },
}

# ==================================================
# HONEYPOTS
# ==================================================

HONEYPOTS = {
    "patient_monitor": True,
    "infusion_pump": True,
    "smart_hvac": True,
    "smart_bed": True,
    "medical_imaging": True,
    "nurse_station": True,
    "fake_attack_generation": True,
}

# ==================================================
# THREAT INTELLIGENCE
# ==================================================

THREAT_INTEL = {
    "mitre_enabled": True,
    "whois_enabled": True,
    "geoip_enabled": True,
    "virustotal_enabled": False,
    "shodan_enabled": False,
    "abuseipdb_enabled": False,
}

# ==================================================
# THREAT SCORING
# ==================================================

THREAT_SCORING = {
    "low": 25,
    "medium": 50,
    "high": 75,
    "critical": 90,
}

# ==================================================
# LOGGING
# ==================================================

LOGGING = {
    "app_log": LOG_DIR / "app.log",
    "audit_log": LOG_DIR / "audit.log",
    "attack_log": LOG_DIR / "attacks.log",
    "honeypot_log": LOG_DIR / "honeypot.log",
    "system_log": LOG_DIR / "system.log",
}

# ==================================================
# DATA FILES
# ==================================================

DATA_FILES = {
    "users": DATA_DIR / "users.json",
    "permissions": DATA_DIR / "permissions.json",
    "attacks": DATA_DIR / "attacks.json",
    "audit_logs": DATA_DIR / "audit_logs.json",
    "threat_feed": DATA_DIR / "threat_feed.json",
    "dashboard_cache": DATA_DIR / "dashboard_cache.json",
    "geo_cache": DATA_DIR / "geo_cache.json",
    "mitre_mapping": DATA_DIR / "mitre_mapping.json",
}

# ==================================================
# REPORTS
# ==================================================

REPORTS = {
    "pdf_dir": REPORT_DIR / "pdf",
    "csv_dir": REPORT_DIR / "csv",
    "html_dir": REPORT_DIR / "html",
}

# ==================================================
# FEATURES
# ==================================================

FEATURES = {
    "soc_terminal": True,
    "attack_timeline": True,
    "ioc_extraction": True,
    "mitre_mapping": True,
    "behavior_analysis": True,
    "malware_analysis": True,
    "geo_visualization": True,
    "incident_response": True,
}

# ==================================================
# FUTURE
# ==================================================

FUTURE = {
    "cowrie_integration": False,
    "elastic_integration": False,
    "misp_integration": False,
    "suricata_integration": False,
    "zeek_integration": False,
    "ai_threat_analysis": False,
}