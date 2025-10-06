# Pico W: MQ-2 -> MQTT (Jetson @ 192.168.0.102)
import network, time, machine
from umqtt.simple import MQTTClient

WIFI_SSID = "TP-Link_FC93"
WIFI_PSK  = "21745638"
JETSON_IP = "192.168.0.121"      # Jetson Nano IP
TOPIC_DATA   = b"sensors/gas"
TOPIC_ALERTS = b"alerts/gas"

adc = machine.ADC(26)  # MQ-2 A0 -> GP26/ADC0

def mv():
    return (adc.read_u16()/65535.0)*3300.0

def avg(n=8, dt=0.02):
    s=0.0
    for _ in range(n):
        s += mv(); time.sleep(dt)
    return s/n

# --- Warm-up & baseline ---
for _ in range(30): _=mv(); time.sleep(0.1)          # ~3s quick warm-up
baseline = sum(mv() for _ in range(50))/50           # ~1s baseline in clean air
print("Baseline (mV):", int(baseline))

# --- Wi-Fi connect ---
w = network.WLAN(network.STA_IF); w.active(True)
if not w.isconnected():
    w.connect(WIFI_SSID, WIFI_PSK)
    while not w.isconnected(): time.sleep(0.2)
print("Wi-Fi:", w.ifconfig())

# --- MQTT connect ---
c = MQTTClient(b"pico-mq2", JETSON_IP, 1883)
c.connect()
print("MQTT connected")

THRESH = 1.5             # alert when > 1.5x baseline
PUBLISH_EVERY = 1.0      # seconds

while True:
    val = avg(8)
    status = "ok" if val < baseline*THRESH else "elevated"
    msg = ('{"sensor":"mq2","adc_mv":%d,"baseline_mv":%d,"status":"%s"}'
           % (int(val), int(baseline), status))
    try:
        c.publish(TOPIC_DATA, msg)
        if status == "elevated":
            c.publish(TOPIC_ALERTS, msg)
    except Exception as e:
        try:
            c.connect(); c.publish(TOPIC_DATA, msg)
        except:
            pass
    time.sleep(PUBLISH_EVERY)

