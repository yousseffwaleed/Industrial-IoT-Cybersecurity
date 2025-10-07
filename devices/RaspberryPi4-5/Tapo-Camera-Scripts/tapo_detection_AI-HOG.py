import os, time, cv2
from datetime import datetime
from pathlib import Path

URL = "rtsp://Youssefelshenawy:YmYmYm12!@192.168.0.103/stream2"

OUT_DIR = Path.home() / "detections"
OUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
if not cap.isOpened():
    print("Cannot open stream"); raise SystemExit(1)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

last_snapshot_ts = 0
snapshot_interval_s = 10
frame_count = 0
t0 = time.time()

print("Running HOG person detection (headless). Ctrl+C to stop.")
try:
    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.05)
            continue

        frame_count += 1
        # Resize to ~640px max dimension for speed/accuracy sweet spot
        h, w = frame.shape[:2]
        target = 640.0
        scale = target / max(h, w)
        if scale < 1.0:
            frame_small = cv2.resize(frame, (int(w*scale), int(h*scale)))
        else:
            frame_small = frame

        # HOG parameters tuned to be a bit more permissive
        # Try winStride (4,4), padding (8,8), scale 1.05; tweak if too slow/noisy
        rects, weights = hog.detectMultiScale(
            frame_small,
            winStride=(4, 4),
            padding=(8, 8),
            scale=1.05
        )

        # Lower the confidence gate to catch more (then you can raise later)
        rects = [r for r, conf in zip(rects, weights) if conf > 0.3]
        n = len(rects)

        # Log some heartbeat every 30 frames
        if frame_count % 30 == 0:
            fps = frame_count / (time.time() - t0 + 1e-6)
            print(f"[{datetime.now():%H:%M:%S}] frames={frame_count} fps={fps:.1f} detections={n}")

        if n > 0:
            annotated = frame_small.copy()
            for (x, y, ww, hh) in rects:
                cv2.rectangle(annotated, (x, y), (x+ww, y+hh), (255, 255, 255), 2)

            if time.time() - last_snapshot_ts >= snapshot_interval_s:
                out = OUT_DIR / f"person_{int(time.time())}.jpg"
                cv2.imwrite(str(out), annotated)
                print(f"[{datetime.now():%H:%M:%S}] Persons detected: {n} -> saved {out}")
                last_snapshot_ts = time.time()

        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    cap.release()
