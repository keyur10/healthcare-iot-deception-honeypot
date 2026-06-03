from functools import wraps

from flask import (
    session,
    redirect,
    url_for,
    flash,
    abort,
)

import logging

logger = logging.getLogger(
    __name__
)


def current_user():

    return session.get(
        "user"
    )


def current_role():

    return session.get(
        "role"
    )


def is_authenticated():

    return (
        current_user()
        is not None
    )


def login_required(func):

    @wraps(func)
    def wrapper(
        *args,
        **kwargs
    ):

        if (
            not is_authenticated()
        ):

            flash(
                "Please login first.",
                "warning",
            )

            return redirect(
                url_for(
                    "login"
                )
            )

        return func(
            *args,
            **kwargs
        )

    return wrapper


def role_required(*roles):

    def decorator(func):

        @wraps(func)
        def wrapper(
            *args,
            **kwargs
        ):

            if (
                not is_authenticated()
            ):

                return redirect(
                    url_for(
                        "login"
                    )
                )

            if (
                current_role()
                not in roles
            ):

                logger.warning(
                    "ACCESS DENIED | "
                    "USER=%s | ROLE=%s",
                    current_user(),
                    current_role(),
                )

                abort(403)

            return func(
                *args,
                **kwargs
            )

        return wrapper

    return decorator