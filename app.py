from flask import Flask, redirect, url_for

from flask_login import current_user

from extensions import db, login_manager


def create_app():

    app = Flask(__name__)


    # =========================================================
    # CONFIGURATION
    # =========================================================

    app.config["SECRET_KEY"] = (
        "smart-attendance-secret-key-change-later"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///smart_attendance.db"
    )

    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
    ] = False


    # =========================================================
    # EXTENSIONS
    # =========================================================

    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"


    # =========================================================
    # MODELS
    # =========================================================

    from models.user import User
    from models.student import Student
    from models.attendance import Attendance
    from models.face_embedding import FaceEmbedding


    # =========================================================
    # ROUTES
    # =========================================================

    from routes.auth import auth
    from routes.dashboard import dashboard
    from routes.students import students
    from routes.attendance import attendance
    from routes.admin import admin


    # =========================================================
    # BLUEPRINTS
    # =========================================================

    app.register_blueprint(auth)

    app.register_blueprint(dashboard)

    app.register_blueprint(students)

    app.register_blueprint(attendance)

    app.register_blueprint(admin)


    # =========================================================
    # HOME
    # =========================================================

    @app.route("/")
    def home():

        if current_user.is_authenticated:

            return redirect(
                url_for("dashboard.index")
            )

        return redirect(
            url_for("auth.login")
        )


    # =========================================================
    # DATABASE
    # =========================================================

    with app.app_context():

        db.create_all()


    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )