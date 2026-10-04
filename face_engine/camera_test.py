import cv2


camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    exit()


print("Webcam started.")
print("Press Q to quit.")


while True:

    success, frame = camera.read()

    if not success:
        print("ERROR: Could not read frame.")
        break

    cv2.imshow(
        "Smart Attendance - Camera Test",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()