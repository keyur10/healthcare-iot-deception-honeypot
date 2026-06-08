from __future__ import annotations

import ipaddress
import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.config import LOG_DIR

# ==================================================
# LOGGER
# ==================================================

logger = logging.getLogger(__name__)


# ==================================================
# TIME
# ==================================================

def utc_now() -> datetime:
    """
    Return current UTC datetime.
    """

    return datetime.now(timezone.utc)


def utc_timestamp() -> str:
    """
    Return ISO-8601 UTC timestamp.
    """

    return utc_now().isoformat()


def human_timestamp() -> str:
    """
    Human-readable timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ==================================================
# IDS
# ==================================================

def generate_id() -> str:
    """
    Generate unique identifier.
    """

    return str(uuid.uuid4())


# ==================================================
# FILESYSTEM
# ==================================================

def ensure_directory(
    directory: Path,
) -> None:
    """
    Create directory if missing.
    """

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


def ensure_project_directories() -> None:
    """
    Ensure runtime directories exist.
    """

    ensure_directory(LOG_DIR)


# ==================================================
# JSON
# ==================================================

def load_json(
    file_path: Path,
    default: Any = None,
) -> Any:
    """
    Safely load JSON file.
    """

    if not file_path.exists():

        return (
            default
            if default is not None
            else {}
        )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception:

        logger.exception(
            "Failed loading JSON: %s",
            file_path,
        )

        return (
            default
            if default is not None
            else {}
        )


def save_json(
    file_path: Path,
    data: Any,
) -> bool:
    """
    Safely save JSON file.
    """

    try:

        ensure_directory(
            file_path.parent
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return True

    except Exception:

        logger.exception(
            "Failed saving JSON: %s",
            file_path,
        )

        return False


# ==================================================
# NETWORK
# ==================================================

def is_valid_ip(
    ip_address: str,
) -> bool:
    """
    Validate IPv4/IPv6 address.
    """

    try:

        ipaddress.ip_address(
            ip_address
        )

        return True

    except ValueError:

        return False


# ==================================================
# ATTACK HELPERS
# ==================================================

def create_attack_record(
    ip: str,
    device: str,
    attack_type: str,
    payload: str = "",
    country: str = "Unknown",
    risk: str = "LOW",
) -> dict[str, Any]:
    """
    Standard attack event structure.
    """

    return {
        "id": generate_id(),
        "timestamp": utc_timestamp(),
        "ip": ip,
        "device": device,
        "attack_type": attack_type,
        "payload": payload,
        "country": country,
        "risk": risk,
    }


# ==================================================
# LOGGING
# ==================================================

def configure_logging() -> None:
    """
    Configure application logging.
    """

    ensure_project_directories()

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    logger.info(
        "Logging initialized"
    )