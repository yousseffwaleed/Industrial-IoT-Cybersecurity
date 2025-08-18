# Sensor Setup (DHT11/DHT22 with Raspberry Pi 5)

This guide explains how to set up a DHT11/DHT22 temperature & humidity sensor with a Raspberry Pi 5, install the required libraries, and verify the sensor is working with a Python script.

---

## 1. Hardware Requirements
- Raspberry Pi 5 (8GB in this project)
- DHT11 or DHT22 sensor module
- Breadboard & jumper wires
- 10kΩ pull-up resistor (if your DHT sensor board does not already include one)

---

## 2. Wiring the Sensor
Connect the sensor to your Raspberry Pi GPIO pins:

| DHT11/DHT22 Pin | Raspberry Pi Pin | Description |
|------------------|------------------|-------------|
| VCC              | 3.3V (Pin 1)     | Power supply |
| GND              | GND (Pin 6)      | Ground |
| DATA             | GPIO4 (Pin 7)    | Data line |

⚠️ If your sensor does not have a built-in resistor, place a **10kΩ pull-up resistor** between **VCC** and **DATA**.

---

## 3. Update System and Install Dependencies
Run these commands on your Raspberry Pi:

```bash
# Update package list
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install Python development tools
sudo apt install -y python3-pip python3-dev
