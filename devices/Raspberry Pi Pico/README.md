# Raspberry Pi Pico W (MicroPython MQTT Node)

This folder contains MicroPython code and dependencies for Pico W nodes in the Industrial IoT Testbed.

## Files
- `src/wifi_test.py` → Connect Pico W to Wi-Fi and print IP.
- `src/main.py` → MQTT publisher (simulated water flow rate).
- `lib/umqtt/simple.py` → MQTT client library (offline install).

## Setup
1. Flash MicroPython (UF2) onto the Pico W.
2. Open Thonny → Interpreter = MicroPython (Raspberry Pi Pico).
3. Copy `lib/umqtt/simple.py` → `/lib/umqtt/simple.py` on Pico.
4. Edit `src/main.py` to set:
   - Wi-Fi SSID & password
   - `BROKER_IP` = MQTT broker IP (e.g., Raspberry Pi)
5. Save `src/main.py` to Pico as `main.py`.

## Run
- Power/reset the Pico → it will auto-run `main.py`.
- On the broker, subscribe to topic:
  ```bash
  mosquitto_sub -h <BROKER_IP> -t "testbed/#" -v

