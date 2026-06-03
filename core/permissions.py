from functools import wraps
import logging

from flask import (
    abort,
    redirect,
    url_for,
)

from core.auth import (
    current_role,
    current_user,
    is_authenticated,
)

from core.storage import (
    load_permissions,
)

from core.audit import (
    log_event,
)

logger = logging.getLogger(__name__)


def has_permission(permission: str) -> bool:
    """
    Check whether the current user's role
    has the requested permission.
    """

    role = current_role()

    if not role:
        return False

    permissions = load_permissions()

    role_permissions = permissions.get(
        role,
        {},
    )

    if role_permissions.get("*", False):
        return True

    return role_permissions.get(
        permission,
        False,
    )


def permission_required(permission: str):
    """
    Route decorator for permission checks.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if not is_authenticated():

                logger.warning(
                    "AUTH REQUIRED | "
                    "PERMISSION=%s",
                    permission,
                )

                return redirect(
                    url_for("login")
                )

            if not has_permission(permission):

                username = current_user()
                role = current_role()

                logger.warning(
                    "PERMISSION DENIED | "
                    "USER=%s | "
                    "ROLE=%s | "
                    "PERMISSION=%s",
                    username,
                    role,
                    permission,
                )

                try:

                    log_event(
                        actor=username,
                        action="PERMISSION_DENIED",
                        details={
                            "permission": permission,
                            "role": role,
                        },
                    )

                except Exception:

                    logger.exception(
                        "Failed to write audit log"
                    )

                abort(403)

            return func(
                *args,
                **kwargs,
            )

        return wrapper

    return decorator