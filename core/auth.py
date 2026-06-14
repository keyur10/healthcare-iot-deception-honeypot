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


def has_permission(
    permission: str,
) -> bool:

    if (
        current_role()
        == "Administrator"
    ):
        return True

    users = load_users()

    current = current_user()

    for user in users:

        if (
            isinstance(
                user,
                dict,
            )
            and
            user.get(
                "username"
            ) == current
        ):

            return user.get(
                "permissions",
                {}
            ).get(
                permission,
                False
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
        message="User logged out",
    )

    session.clear()


def get_all_users():

    return load_users()
def login_user(username, password):

    users = load_users()

    for user in users:

        if (
            user.get("username") == username
            and
            user.get("password") == password
            and
            user.get("status", "Active") == "Active"
        ):

            session["username"] = username
            session["role"] = user.get(
                "role",
                "Threat Analyst"
            )

            log_event(
                event_type="LOGIN",
                user=username,
                severity="INFO",
                message="User logged in"
            )

            return True

    return False