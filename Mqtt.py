import paho.mqtt.client as mqtt
import Adafruit_DHT
import time
import json

broker_ip = "192.168.0.100"  # Jetson Nano IP
topic = "iot/cluster1/pi01"  # Change for each Pi

sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO pin connected to DHT sensor

client = mqtt.Client()
client.connect(broker_ip, 1883, 60)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        payload = json.dumps({
            "temperature": temperature,
            "humidity": humidity
        })
        client.publish(topic, payload)
        print(f"Published: {payload}")
    else:
        print("Sensor read failed")
    time.sleep(5)
