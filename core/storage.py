from __future__ import annotations

from typing import Any

from core.config import DATA_FILES
from core.helpers import load_json
from core.helpers import save_json


# ==================================================
# GENERIC
# ==================================================

def load_data(
    key: str,
    default: Any,
) -> Any:
    """
    Generic JSON loader.
    """

    return load_json(
        DATA_FILES[key],
        default,
    )


def save_data(
    key: str,
    data: Any,
) -> bool:
    """
    Generic JSON saver.
    """

    return save_json(
        DATA_FILES[key],
        data,
    )


# ==================================================
# USERS
# ==================================================

def load_users() -> list:
    return load_data(
        "users",
        [],
    )


def save_users(
    users: list,
) -> bool:
    return save_data(
        "users",
        users,
    )


# ==================================================
# PERMISSIONS
# ==================================================

def load_permissions() -> dict:
    return load_data(
        "permissions",
        {},
    )


def save_permissions(
    permissions: dict,
) -> bool:
    return save_data(
        "permissions",
        permissions,
    )


# ==================================================
# ATTACKS
# ==================================================

def load_attacks() -> list:
    return load_data(
        "attacks",
        [],
    )


def save_attacks(
    attacks: list,
) -> bool:
    return save_data(
        "attacks",
        attacks,
    )


def append_attack(
    attack: dict,
) -> None:

    attacks = load_attacks()

    attacks.append(
        attack
    )

    save_attacks(
        attacks
    )


# ==================================================
# AUDIT LOGS
# ==================================================

def load_audit_logs() -> list:
    return load_data(
        "audit_logs",
        [],
    )


def save_audit_logs(
    logs: list,
) -> bool:
    return save_data(
        "audit_logs",
        logs,
    )


def append_audit_log(
    log_entry: dict,
) -> None:

    logs = load_audit_logs()

    logs.append(
        log_entry
    )

    save_audit_logs(
        logs
    )


# ==================================================
# THREAT FEED
# ==================================================

def load_threat_feed() -> list:
    return load_data(
        "threat_feed",
        [],
    )


def save_threat_feed(
    feed: list,
) -> bool:
    return save_data(
        "threat_feed",
        feed,
    )


# ==================================================
# DASHBOARD CACHE
# ==================================================

def load_dashboard_cache() -> dict:
    return load_data(
        "dashboard_cache",
        {},
    )


def save_dashboard_cache(
    cache: dict,
) -> bool:
    return save_data(
        "dashboard_cache",
        cache,
    )
# ==================================================
# INITIALIZATION
# ==================================================

def ensure_data_files() -> None:
    """
    Create required data files if missing.
    """

    defaults = {
        "users": [],
        "permissions": {},
        "attacks": [],
        "audit_logs": [],
        "threat_feed": [],
        "dashboard_cache": {},
    }

    for key, file_path in DATA_FILES.items():

        if not file_path.exists():

            save_json(
                file_path,
                defaults.get(key, {})
            )