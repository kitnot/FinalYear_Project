from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

from extensions import db


class User(
    UserMixin,
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="staff"
    )

    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def set_password(
        self,
        password
    ):

        self.password_hash = (
            generate_password_hash(password)
        )

    def check_password(
        self,
        password
    ):

        return check_password_hash(
            self.password_hash,
            password
        )

    @property
    def is_active(self):

        return self.active

    @property
    def is_admin(self):

        return self.role == "admin"