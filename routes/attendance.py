from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

from flask_login import login_required

from extensions import db

from models.student import Student
from models.attendance import Attendance

from face_engine.service import process_face
from face_engine.matcher import (
    find_best_match,
    load_registered_faces
)

from datetime import datetime, date

import cv2
import numpy as np


attendance = Blueprint(
    "attendance",
    __name__,
    url_prefix="/attendance"
)


# ============================================================
# SETTINGS
# ============================================================

COSINE_MINIMUM = 0.363

# Number of successful recognitions required
# before attendance is recorded.
CONFIRMATION_REQUIRED = 3

# Recognition state for the current Flask process.
recognition_state = {}


# ============================================================
# DECODE CAMERA IMAGE
# ============================================================

def decode_image():

    image = request.files.get(
        "image"
    )

    if not image:

        return None, "No image received."

    raw = image.read()

    frame = cv2.imdecode(
        np.frombuffer(
            raw,
            dtype=np.uint8
        ),
        cv2.IMREAD_COLOR
    )

    if frame is None:

        return None, (
            "Could not decode camera image."
        )

    return frame, None


# ============================================================
# RESET OTHER CANDIDATES
# ============================================================

def reset_other_candidates(student_id):

    for key in list(
        recognition_state.keys()
    ):

        if key != student_id:

            recognition_state[key] = 0


# ============================================================
# ATTENDANCE PAGE
# ============================================================

@attendance.route("/")
@login_required
def index():

    today = date.today()

    records = (
        Attendance.query
        .filter_by(date=today)
        .order_by(Attendance.time.desc())
        .all()
    )

    total_students = Student.query.count()

    present_count = len(
        {
            record.student_id
            for record in records
        }
    )

    return render_template(
        "attendance.html",
        records=records,
        total_students=total_students,
        present_count=present_count
    )


# ============================================================
# CONTINUOUS FACE RECOGNITION
# ============================================================

@attendance.route(
    "/recognize",
    methods=["POST"]
)
@login_required
def recognize():

    frame, error = decode_image()

    if error:

        return jsonify(
            success=False,
            recognized=False,
            message=error
        ), 400

    try:

        # ----------------------------------------------------
        # PROCESS FACE
        # ----------------------------------------------------

        feature, error = process_face(
            frame
        )

        if error:

            return jsonify(
                success=True,
                recognized=False,
                marked=False,
                message=error
            )

        # ----------------------------------------------------
        # LOAD REGISTERED FACES
        # ----------------------------------------------------

        registered_faces = (
            load_registered_faces()
        )

        if not registered_faces:

            return jsonify(
                success=True,
                recognized=False,
                marked=False,
                message=(
                    "No registered faces found. "
                    "Register student faces first."
                )
            )

        # ----------------------------------------------------
        # FIND MATCH
        # ----------------------------------------------------

        match = find_best_match(
            feature,
            registered_faces
        )

        if not match:

            return jsonify(
                success=True,
                recognized=False,
                marked=False,
                message="Face not recognized."
            )

        student_id = match[
            "student_id"
        ]

        student_name = match[
            "student_name"
        ]

        score = float(
            match["score"]
        )

        # ----------------------------------------------------
        # EXTRA THRESHOLD CHECK
        # ----------------------------------------------------

        if score < COSINE_MINIMUM:

            return jsonify(
                success=True,
                recognized=False,
                marked=False,
                message="Face confidence too low."
            )

        # ----------------------------------------------------
        # CHECK TODAY'S ATTENDANCE
        # ----------------------------------------------------

        existing = (
            Attendance.query
            .filter_by(
                student_id=student_id,
                date=date.today()
            )
            .first()
        )

        if existing:

            recognition_state[
                student_id
            ] = 0

            total_students = Student.query.count()

            present_count = len(
                {
                    record.student_id
                    for record in
                    Attendance.query.filter_by(
                        date=date.today()
                    ).all()
                }
            )

            return jsonify(

                success=True,

                recognized=True,

                marked=False,

                already_present=True,

                student_name=student_name,

                score=round(
                    score,
                    3
                ),

                present_count=present_count,

                total_students=total_students,

                message=(
                    f"{student_name} "
                    f"is already present."
                )
            )

        # ----------------------------------------------------
        # MULTI-FRAME CONFIRMATION
        # ----------------------------------------------------

        recognition_state[
            student_id
        ] = (
            recognition_state.get(
                student_id,
                0
            ) + 1
        )

        # Reset other recognized candidates
        reset_other_candidates(
            student_id
        )

        confirmations = (
            recognition_state[
                student_id
            ]
        )

        # ----------------------------------------------------
        # NOT YET CONFIRMED
        # ----------------------------------------------------

        if confirmations < CONFIRMATION_REQUIRED:

            return jsonify(

                success=True,

                recognized=True,

                marked=False,

                already_present=False,

                student_name=student_name,

                score=round(
                    score,
                    3
                ),

                confirmations=confirmations,

                required=CONFIRMATION_REQUIRED,

                message=(
                    f"Confirming "
                    f"{student_name} "
                    f"({confirmations}/"
                    f"{CONFIRMATION_REQUIRED})"
                )
            )

        # ----------------------------------------------------
        # MARK ATTENDANCE
        # ----------------------------------------------------

        now = datetime.now()

        attendance_record = Attendance(

            student_id=student_id,

            date=now.date(),

            time=now.time().replace(
                microsecond=0
            ),

            status="Present",

            confidence=score
        )

        db.session.add(
            attendance_record
        )

        db.session.commit()

        # Reset confirmation
        recognition_state[
            student_id
        ] = 0

        # ----------------------------------------------------
        # UPDATE COUNTERS
        # ----------------------------------------------------

        total_students = Student.query.count()

        today_records = (
            Attendance.query
            .filter_by(
                date=now.date()
            )
            .all()
        )

        present_count = len(
            {
                record.student_id
                for record in today_records
            }
        )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify(

            success=True,

            recognized=True,

            marked=True,

            already_present=False,

            student_name=student_name,

            score=round(
                score,
                3
            ),

            confirmations=CONFIRMATION_REQUIRED,

            required=CONFIRMATION_REQUIRED,

            present_count=present_count,

            total_students=total_students,

            message=(
                f"✓ {student_name} "
                f"marked Present."
            )
        )

    except Exception as exc:

        db.session.rollback()

        return jsonify(

            success=False,

            recognized=False,

            marked=False,

            message=(
                f"Recognition error: "
                f"{exc}"
            )

        ), 500