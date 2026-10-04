import cv2

from face_engine.detector import FaceDetector
from face_engine.recognizer import FaceRecognizer


detector = FaceDetector()

recognizer = FaceRecognizer()


def process_face(frame):

    if frame is None:

        return None, "Invalid camera image."


    if len(frame.shape) != 3:

        return None, "Invalid image format."


    faces = detector.detect(
        frame
    )


    if len(faces) == 0:

        return None, (
            "No face detected. "
            "Move closer and make sure your face is visible."
        )


    if len(faces) > 1:

        return None, (
            "Multiple faces detected. "
            "Only one person should be in the camera."
        )


    face = faces[0]


    feature = recognizer.get_feature(
        frame,
        face
    )


    return feature, None