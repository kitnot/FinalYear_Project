from extensions import db


class Attendance(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    student_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "student.id"
        ),
        nullable=False
    )


    date = db.Column(
        db.Date,
        nullable=False
    )


    time = db.Column(
        db.Time,
        nullable=False
    )


    status = db.Column(
        db.String(20),
        default="Present"
    )


    confidence = db.Column(
        db.Float
    )


    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    student = db.relationship(
        "Student",
        backref=db.backref(
            "attendance_records",
            lazy=True
        )
    )