import time
import adafruit_dht
import board

# Use GPIO4 (pin 7) for the DHT sensor
dht = adafruit_dht.DHT11(board.D4)  # or DHT22

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity
        print(f"Temp: {temperature}°C   Humidity: {humidity}%")
    except RuntimeError:
        # Reading errors are common with DHT sensors
        pass
    time.sleep(2)
