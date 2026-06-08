from __future__ import annotations

from typing import Any

from core.helpers import (
    generate_id,
    utc_timestamp,
)

from core.storage import (
    load_audit_logs,
    save_audit_logs,
)


# ==================================================
# AUDIT LOGGING
# ==================================================

def log_event(
    event_type: str,
    message: str,
    user: str = "system",
    severity: str = "INFO",
    metadata: dict[str, Any] | None = None,
) -> dict:
    """
    Create and store an audit event.
    """

    event = {
        "id": generate_id(),
        "timestamp": utc_timestamp(),
        "event_type": event_type,
        "user": user,
        "severity": severity,
        "message": message,
        "metadata": metadata or {},
    }

    logs = load_audit_logs()

    if not isinstance(logs, list):
        logs = []

    logs.append(event)

    save_audit_logs(logs)

    return event


# ==================================================
# READ LOGS
# ==================================================

def get_audit_logs() -> list:
    """
    Return all audit logs.
    """

    logs = load_audit_logs()

    if not isinstance(logs, list):
        return []

    return logs


def get_recent_logs(
    limit: int = 50,
) -> list:
    """
    Return recent audit logs.
    """

    logs = get_audit_logs()

    return logs[-limit:]


# ==================================================
# SEARCH
# ==================================================

def search_logs(
    keyword: str,
) -> list:
    """
    Search audit logs.
    """

    keyword = keyword.lower()

    results = []

    for log in get_audit_logs():

        if keyword in str(log).lower():

            results.append(log)

    return results


# ==================================================
# CLEAR
# ==================================================

def clear_audit_logs() -> None:
    """
    Remove all audit logs.
    """

    save_audit_logs([])