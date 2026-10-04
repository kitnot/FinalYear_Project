import numpy as np

from models.face_embedding import FaceEmbedding
from models.student import Student

from face_engine.recognizer import FaceRecognizer


recognizer = FaceRecognizer()


# OpenCV's documented SFace cosine threshold
# is 0.363. We use it as a starting point.
COSINE_THRESHOLD = 0.363


def load_registered_faces():

    records = (
        FaceEmbedding.query
        .join(
            Student,
            FaceEmbedding.student_id == Student.id
        )
        .all()
    )


    registered_faces = []


    for record in records:

        feature = np.frombuffer(
            record.embedding,
            dtype=np.float32
        )


        feature = feature.reshape(
            1,
            -1
        )


        registered_faces.append({

            "student_id":
                record.student_id,

            "student_name":
                record.student.name
                if record.student
                else "Unknown",

            "feature":
                feature

        })


    return registered_faces


def find_best_match(
    query_feature,
    registered_faces
):

    if not registered_faces:

        return None


    best_match = None

    best_score = -1.0


    for registered in registered_faces:

        score = recognizer.compare(
            query_feature,
            registered["feature"]
        )


        if score > best_score:

            best_score = score

            best_match = registered


    if (
        best_match is not None
        and best_score >= COSINE_THRESHOLD
    ):

        return {

            "student_id":
                best_match["student_id"],

            "student_name":
                best_match["student_name"],

            "score":
                best_score

        }


    return None