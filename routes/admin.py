from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.user import User
from routes.admin_required import admin_required


admin = Blueprint("admin", __name__, url_prefix="/admin")


# ==============================
# ADMIN DASHBOARD
# ==============================
@admin.route("/")
@login_required
@admin_required
def index():
    users = User.query.order_by(User.username.asc()).all()

    return render_template(
        "admin.html",
        users=users
    )


# ==============================
# CREATE NEW USER
# ==============================
@admin.route("/create-user", methods=["POST"])
@login_required
@admin_required
def create_user():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    role = request.form.get("role", "staff")

    if not username or not password:
        flash("Username and password are required.")
        return redirect(url_for("admin.index"))

    if role not in ["admin", "staff"]:
        role = "staff"

    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:
        flash("Username already exists.")
        return redirect(url_for("admin.index"))

    new_user = User(
        username=username,
        role=role,
        active=True
    )

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash(
        f"User '{username}' created successfully."
    )

    return redirect(url_for("admin.index"))


# ==============================
# ENABLE / DISABLE USER
# ==============================
@admin.route("/toggle/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent administrator from disabling themselves
    if user.id == current_user.id:
        flash("You cannot disable your own account.")
        return redirect(url_for("admin.index"))

    # Toggle account status
    user.active = not user.active

    db.session.commit()

    if user.active:
        status = "enabled"
    else:
        status = "disabled"

    flash(
        f"User '{user.username}' is now {status}."
    )

    return redirect(url_for("admin.index"))


# ==============================
# CHANGE USER ROLE
# ==============================
@admin.route("/role/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def change_role(user_id):

    user = User.query.get_or_404(user_id)

    # Prevent administrator from changing their own role
    if user.id == current_user.id:
        flash("You cannot change your own role.")
        return redirect(url_for("admin.index"))

    role = request.form.get("role")

    if role not in ["admin", "staff"]:
        flash("Invalid role selected.")
        return redirect(url_for("admin.index"))

    user.role = role

    db.session.commit()

    flash(
        f"User '{user.username}' role updated to {role}."
    )

    return redirect(url_for("admin.index"))