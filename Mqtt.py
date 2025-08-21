import time
import board
import adafruit_dht
import paho.mqtt.client as mqtt

# Set up sensor
dht_device = adafruit_dht.DHT11(board.D4)

# Set up MQTT client
broker_ip = "192.168.0.127"  # <-- Replace with your Jetson's IP
topic = "iot/cluster2/pi01"

client = mqtt.Client()
client.connect(broker_ip, 1883, 60)

while True:
    try:
        temperature_c = dht_device.temperature
        humidity = dht_device.humidity
        message = f"Temp: {temperature_c}°C | Humidity: {humidity}%"
        client.publish(topic, message)
        print("Published:", message)
    except Exception as e:
        print("Sensor error:", e)
    time.sleep(5)
