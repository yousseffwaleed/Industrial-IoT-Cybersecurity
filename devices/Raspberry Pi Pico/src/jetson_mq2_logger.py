
# jetson_mq2_logger.py

# Subscribes to sensors/gas and appends rows to mq2_log.csv

import paho.mqtt.client as mqtt
import json, csv, os
from datetime import datetime

BROKER_HOST = "127.0.0.1"        # Mosquitto is on this Jetson
TOPIC       = "sensors/gas"
CSV_PATH    = "mq2_log.csv"

# Create CSV with header if it doesn't exist
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "a", newline="") as f:
        csv.writer(f).writerow(
            ["timestamp", "topic", "adc_mv", "baseline_mv", "status", "raw_json"]
        )

def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    ts = datetime.now().isoformat()
    raw = msg.payload.decode(errors="replace")
    adc = baseline = status = ""
    try:
        data = json.loads(raw)
        adc = data.get("adc_mv", "")
        baseline = data.get("baseline_mv", "")
        status = data.get("status", "")
    except json.JSONDecodeError:
        pass

    with open(CSV_PATH, "a", newline="") as f:
        csv.writer(f).writerow([ts, msg.topic, adc, baseline, status, raw])

    print(f"{ts}  adc={adc}  baseline={baseline}  status={status}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, 1883, 60)
client.loop_forever()
