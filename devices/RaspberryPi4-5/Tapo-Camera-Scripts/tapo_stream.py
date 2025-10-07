import cv2

URL = "rtsp://Youssefelshenawy:YmYmYm12!@192.168.0.103/stream1"

cap = cv2.VideoCapture(URL)
if not cap.isOpened():
    print("Cannot open stream"); exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Tapo Stream", frame)
    if cv2.waitKey(1) == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()

