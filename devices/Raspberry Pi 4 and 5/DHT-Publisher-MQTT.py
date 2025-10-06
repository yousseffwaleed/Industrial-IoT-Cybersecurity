# rpi_dht_publisher.py  -- Raspberry Pi -> Jetson (cluster c2)
import time, json
import paho.mqtt.client as mqtt
import adafruit_dht, board

BROKER   = "192.168.0.121"   # Jetson IP
CLUSTER  = "c2"
DEVICE   = "rpi01"           # change if this Pi should have another ID
SENSOR_TYPE = "DHT11"        # set to "DHT22" if you have DHT22
PIN = board.D4               # DATA on GPIO4 (physical pin 7)

dht = adafruit_dht.DHT22(PIN, use_pulseio=False) if SENSOR_TYPE=="DHT22" else adafruit_dht.DHT11(PIN, use_pulseio=False)

TOPIC_DATA   = f"cluster/{CLUSTER}/{DEVICE}/dht"
TOPIC_STATUS = f"cluster/{CLUSTER}/{DEVICE}/status"

c = mqtt.Client(client_id=f"{CLUSTER}-{DEVICE}-dht", clean_session=True)
c.will_set(TOPIC_STATUS, "offline", retain=True)
c.connect(BROKER, 1883, 60)
c.publish(TOPIC_STATUS, "online", retain=True)

try:
    while True:
        try:
            t_c = dht.temperature
            h   = dht.humidity
            if t_c is None or h is None:
                raise RuntimeError("bad read")
            payload = {
                "sensor":"dht",
                "type": SENSOR_TYPE.lower(),
                "temperature_c": round(float(t_c), 2),
                "humidity_pct":  round(float(h), 2)
            }
            c.publish(TOPIC_DATA, json.dumps(payload))
            print("pub:", payload)
        except RuntimeError as e:
            # DHTs occasionally error; just try next cycle
            print("read retry:", e)
        time.sleep(2)
finally:
    c.publish(TOPIC_STATUS, "offline", retain=True)
    c.disconnect()
