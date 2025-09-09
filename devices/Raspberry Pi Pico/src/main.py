import mip
import network, time, random
from umqtt.simple import MQTTClient

# Wi-Fi credentials
SSID = "TELUSWiFi0179"
PASSWORD = "XXXXX"

# Broker (your Pi-1 aggregator)
BROKER_IP = "192.168.1.75"   # <-- replace with Pi-1's static IP

# MQTT client config
CLIENT_ID = "pico_sensor_01"
TOPIC = b"testbed/sensors/water_flow"

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(1)

print("\n✅ Connected to WiFi")
print("IP Info:", wlan.ifconfig())

# Connect to broker
client = MQTTClient(CLIENT_ID, BROKER_IP)
client.connect()
print("✅ Connected to MQTT broker:", BROKER_IP)

# Publish simulated sensor values forever
while True:
    flow_rate = round(10 + random.uniform(0, 2), 2)  # e.g., water flow rate
    msg = f"{flow_rate}"
    client.publish(TOPIC, msg)
    print("Published:", msg)
    time.sleep(5)
