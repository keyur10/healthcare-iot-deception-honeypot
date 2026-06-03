# core/storage.py

from pathlib import Path
import json


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

USERS_FILE = DATA_DIR / "users.json"

PERMISSIONS_FILE = DATA_DIR / "permissions.json"

AUDIT_FILE = DATA_DIR / "audit.json"


DEFAULT_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "active": True,
    },
    "analyst": {
        "password": "analyst123",
        "role": "analyst",
        "active": True,
    },
    "viewer": {
        "password": "viewer123",
        "role": "viewer",
        "active": True,
    },
}


DEFAULT_PERMISSIONS = {
    "admin": {
        "*": True
    },
    "analyst": {},
    "viewer": {},
}


def ensure_data_files() -> None:

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if not USERS_FILE.exists():

        save_users(
            DEFAULT_USERS
        )

    if not PERMISSIONS_FILE.exists():

        save_permissions(
            DEFAULT_PERMISSIONS
        )

    if not AUDIT_FILE.exists():

        save_audit_logs(
            []
        )


def load_json(
    file_path: Path,
    default
):

    try:

        if not file_path.exists():

            return default

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return default


def save_json(
    file_path: Path,
    data
) -> None:

    with open(
        file_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
        )


# ==================================================
# USERS
# ==================================================

def load_users():

    return load_json(
        USERS_FILE,
        DEFAULT_USERS,
    )


def save_users(
    users
) -> None:

    save_json(
        USERS_FILE,
        users,
    )


# ==================================================
# PERMISSIONS
# ==================================================

def load_permissions():

    return load_json(
        PERMISSIONS_FILE,
        DEFAULT_PERMISSIONS,
    )


def save_permissions(
    permissions
) -> None:

    save_json(
        PERMISSIONS_FILE,
        permissions,
    )


# ==================================================
# AUDIT LOGS
# ==================================================

def load_audit_logs():

    return load_json(
        AUDIT_FILE,
        [],
    )


def save_audit_logs(
    logs
) -> None:

    save_json(
        AUDIT_FILE,
        logs,
    )