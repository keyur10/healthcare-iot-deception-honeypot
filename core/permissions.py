from __future__ import annotations

from core.storage import load_permissions
from core.audit import log_event


def get_role_permissions(
    role: str,
) -> dict:
    """
    Get permissions for a role.
    """

    permissions = load_permissions()

    return permissions.get(
        role,
        {},
    )


def has_permission(
    role: str,
    permission: str,
) -> bool:
    """
    Check role permission.
    """

    role_permissions = get_role_permissions(
        role
    )

    if role_permissions.get("*"):

        return True

    return role_permissions.get(
        permission,
        False,
    )


def validate_permission(
    role: str,
    permission: str,
    user: str = "system",
) -> bool:
    """
    Check and audit permission usage.
    """

    allowed = has_permission(
        role,
        permission,
    )

    if not allowed:

        log_event(
            event_type="PERMISSION_DENIED",
            user=user,
            severity="WARNING",
            message=(
                f"{role} denied access to "
                f"{permission}"
            ),
        )

    return allowed