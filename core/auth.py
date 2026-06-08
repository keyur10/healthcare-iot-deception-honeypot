from __future__ import annotations

from flask import session

from core.audit import log_event
from core.storage import load_users


def current_user() -> str | None:
    """
    Return current username.
    """

    return session.get(
        "username"
    )


def current_role() -> str:
    """
    Return current role.
    """

    return session.get(
        "role",
        "user",
    )


def is_authenticated() -> bool:
    """
    Check authentication.
    """

    return (
        "username"
        in session
    )


def login_user(
    username: str,
    password: str,
) -> bool:
    """
    Authenticate user.
    """

    users = load_users()

    for user in users:

        if (
            user.get("username")
            == username
            and
            user.get("password")
            == password
        ):

            session["username"] = username

            session["role"] = user.get(
                "role",
                "user",
            )

            log_event(
                event_type="LOGIN",
                user=username,
                severity="INFO",
                message=(
                    "User logged in"
                ),
            )

            return True

    log_event(
        event_type="LOGIN_FAILED",
        user=username,
        severity="WARNING",
        message=(
            "Invalid credentials"
        ),
    )

    return False


def logout_user() -> None:
    """
    Logout current user.
    """

    username = session.get(
        "username",
        "unknown",
    )

    log_event(
        event_type="LOGOUT",
        user=username,
        severity="INFO",
        message=(
            "User logged out"
        ),
    )

    session.clear()

def get_all_users():

    return load_users()