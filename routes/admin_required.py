from functools import wraps

from flask import (
    redirect,
    url_for,
    flash
)

from flask_login import current_user


def admin_required(function):

    @wraps(function)
    def wrapper(
        *args,
        **kwargs
    ):

        if not current_user.is_authenticated:

            return redirect(
                url_for("auth.login")
            )


        if not current_user.is_admin:

            flash(
                "Administrator access required."
            )

            return redirect(
                url_for("dashboard.index")
            )


        return function(
            *args,
            **kwargs
        )

    return wrapper