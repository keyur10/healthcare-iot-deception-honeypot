# core/audit.py

from datetime import datetime

from core.storage import (
    load_audit_logs,
    save_audit_logs,
)


def log_event(
    actor: str,
    action: str,
    target: str = "",
    details: dict | None = None,
) -> None:

    logs = load_audit_logs()

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "actor": actor,
        "action": action,
        "target": target,
        "details": details or {},
    }

    logs.append(entry)

    save_audit_logs(logs)


def get_audit_logs():

    logs = load_audit_logs()

    return sorted(
        logs,
        key=lambda item: item["timestamp"],
        reverse=True,
    )


def get_recent_logs(
    limit: int = 100,
):

    return get_audit_logs()[:limit]


def search_logs(
    keyword: str,
):

    keyword = keyword.lower()

    results = []

    for log in get_audit_logs():

        if (
            keyword in str(log).lower()
        ):

            results.append(log)

    return results