from extensions import db


class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    student_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )


    name = db.Column(
        db.String(100),
        nullable=False
    )


    email = db.Column(
        db.String(120)
    )


    phone = db.Column(
        db.String(20)
    )


    course = db.Column(
        db.String(100)
    )


    semester = db.Column(
        db.String(20)
    )


    division = db.Column(
        db.String(20)
    )


    face_encoding = db.Column(
        db.LargeBinary
    )


    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    face_embeddings = db.relationship(
        "FaceEmbedding",
        backref="student",
        lazy=True,
        cascade="all, delete-orphan"
    )