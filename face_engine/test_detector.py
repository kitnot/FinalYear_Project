import cv2

from detector import FaceDetector


detector = FaceDetector()

camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print("Could not open webcam.")

    exit()


print("Face detection started.")
print("Press Q to quit.")


while True:

    success, frame = camera.read()

    if not success:
        break

    faces = detector.detect(frame)

    for face in faces:

        x, y, w, h = face[:4].astype(int)

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        confidence = face[-1]

        cv2.putText(
            frame,
            f"Face: {confidence:.2f}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "YuNet Face Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()