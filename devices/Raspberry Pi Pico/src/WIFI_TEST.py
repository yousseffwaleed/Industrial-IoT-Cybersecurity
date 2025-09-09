import network, time

SSID = "TELUSWiFi0179"
PASSWORD = "XXXXX"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(1)

print("\n✅ Connected!")
print("IP Info:", wlan.ifconfig())
