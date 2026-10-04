import cv2
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "yunet"
    / "face_detection_yunet_2023mar.onnx"
)


class FaceDetector:

    def __init__(self):

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"YuNet model not found:\n{MODEL_PATH}"
            )

        self.detector = cv2.FaceDetectorYN.create(
            str(MODEL_PATH),
            "",
            (320, 320),
            0.7,
            0.3,
            5000
        )


    def detect(self, frame):

        height, width = frame.shape[:2]

        self.detector.setInputSize(
            (width, height)
        )

        _, faces = self.detector.detect(
            frame
        )

        if faces is None:

            return []

        return faces