from flask import (
    Blueprint,
    render_template
)

from flask_login import login_required

from models.student import Student
from models.attendance import Attendance

from datetime import date


dashboard = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard.route("/")
@login_required
def index():

    today = date.today()

    total_students = Student.query.count()

    present_today = Attendance.query.filter_by(
        date=today,
        status="Present"
    ).count()

    absent_today = max(
        total_students - present_today,
        0
    )

    recent_attendance = (
        Attendance.query
        .filter_by(date=today)
        .order_by(
            Attendance.time.desc()
        )
        .limit(10)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_students=total_students,
        present_today=present_today,
        absent_today=absent_today,
        recent_attendance=recent_attendance
    )