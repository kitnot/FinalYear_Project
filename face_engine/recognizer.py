import cv2
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "sface"
    / "face_recognition_sface_2021dec.onnx"
)


class FaceRecognizer:

    def __init__(self):

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"SFace model not found:\n{MODEL_PATH}"
            )

        self.recognizer = cv2.FaceRecognizerSF.create(
            str(MODEL_PATH),
            ""
        )


    def get_feature(
        self,
        frame,
        face
    ):

        aligned_face = self.recognizer.alignCrop(
            frame,
            face
        )

        feature = self.recognizer.feature(
            aligned_face
        )

        return feature.astype(
            np.float32
        )


    def compare(
        self,
        feature1,
        feature2
    ):

        score = self.recognizer.match(
            feature1,
            feature2,
            cv2.FaceRecognizerSF_FR_COSINE
        )

        return float(score)