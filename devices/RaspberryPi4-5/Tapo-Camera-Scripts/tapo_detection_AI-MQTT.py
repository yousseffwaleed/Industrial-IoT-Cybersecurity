import os, time, json, socket, cv2
from datetime import datetime
from pathlib import Path
import paho.mqtt.publish as publish

# --- CONFIG ---
URL     = "rtsp://Youssefelshenawy:YmYmYm12!@192.168.0.103/stream2"  # SD stream is lighter
BROKER  = "192.168.0.121"  # <-- Jetson IP here
TOPIC   = "lab/camera/alerts"
SNAP_EVERY_S = 10          # throttle snapshots
CONF_MIN = 0.30            # lower => more sensitive, higher => fewer false positives
MAX_DIM = 640              # resize largest dimension to this for speed

# --- SETUP ---
HOST = socket.gethostname()
OUT_DIR = Path.home() / "detections"
OUT_DIR.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(URL)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
if not cap.isOpened():
    print("Cannot open stream"); raise SystemExit(1)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

last_snap = 0
frame_count, t0 = 0, time.time()

def send_alert(event, count=0, snapshot=None, extra=None):
    msg = {
        "source": "tapo_c100",
        "host": HOST,
        "event": event,           # "person" or "motion"
        "count": count,
        "snapshot": snapshot,     # path on the Pi
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    if extra: msg.update(extra)
    publish.single(TOPIC, payload=json.dumps(msg), hostname=BROKER, qos=1)

print("HOG person detection + MQTT. Ctrl+C to stop.")
try:
    while True:
        ok, frame = cap.read()
        if not ok:
            time.sleep(0.05); continue

        frame_count += 1

        # Resize for speed
        h, w = frame.shape[:2]
        scale = float(MAX_DIM) / max(h, w)
        frame_s = cv2.resize(frame, (int(w*scale), int(h*scale))) if scale < 1.0 else frame

        # Detect people (tuned to be moderately sensitive)
        rects, weights = hog.detectMultiScale(
            frame_s, winStride=(4,4), padding=(8,8), scale=1.05
        )
        picks = [(r, float(conf)) for r, conf in zip(rects, weights) if conf > CONF_MIN]
        n = len(picks)

        # Heartbeat every ~30 frames
        if frame_count % 30 == 0:
            fps = frame_count / (time.time() - t0 + 1e-6)
            print(f"[{datetime.now():%H:%M:%S}] frames={frame_count} fps={fps:.1f} detections={n}")

        if n > 0:
            # Draw & save snapshot (throttled)
            if time.time() - last_snap >= SNAP_EVERY_S:
                annotated = frame_s.copy()
                for (x, y, ww, hh), conf in picks:
                    cv2.rectangle(annotated, (x, y), (x+ww, y+hh), (255,255,255), 2)
                out = OUT_DIR / f"person_{int(time.time())}.jpg"
                cv2.imwrite(str(out), annotated)
                print(f"Saved snapshot: {out}")
                last_snap = time.time()

                # Publish MQTT alert to Jetson
                avg_conf = sum(c for _, c in picks)/n
                send_alert(event="person", count=n, snapshot=str(out), extra={"avg_conf": round(avg_conf, 3)})

        time.sleep(0.01)

except KeyboardInterrupt:
    pass
finally:
    cap.release()
