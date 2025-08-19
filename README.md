## 📡 Project Overview

This project connects **15 Raspberry Pi 5 (8GB)** devices, each equipped with **DHT11/DHT22 temperature and humidity sensors**. Every device is assigned a **static IP address** and configured to transmit data to a central **MQTT broker** hosted on an **NVIDIA Jetson Nano edge node**.

### 🔧 Key Features

- 🔒 **Cybersecurity Monitoring**  
  The Jetson Nano runs **Suricata**, **Zeek**, and **tcpdump** to simulate and detect cyberattacks such as **spoofing** and **flooding** in real time.

- 🌐 **Edge-to-Cloud Integration**  
  Real-time data acquisition and publishing through the MQTT protocol, enabling scalable monitoring and control across distributed IoT nodes.

- ⚡ **Plug-and-Play Deployment**  
  Designed for modular, repeatable setup with minimal configuration. Anyone can replicate this Industrial IoT system by following the step-by-step instructions in this repository.

- 🖥️ **Protocol Diagnostics**  
  Integrated use of **Wireshark** and custom **Bash/Python scripts** for network traffic inspection, anomaly detection, and logging.
---

## 📌 Features
- ✅ Sensor data collection (temperature + humidity)  
- ✅ Static IP assignment for 15 Raspberry Pi 5 devices  
- ✅ Automated static IP setup script (`static_ip.sh`)  
- 🔄 MQTT communication setup (next phase)  
- 📖 Complete documentation so anyone can reproduce the project  

---

## 🛠️ Hardware
- 15 × Raspberry Pi 5 (8GB)  
- 15 × DHT11 or DHT22 sensors  
- Jumper wires & breadboards  
- Router (local network)  

---

## 📂 Repository Structure
```
RaspberryPi-IoT-Project/
├── README.md                  # Project overview
├── setup/
│   ├── sensor_setup.md        # Install libraries + connect/test sensor
│   ├── network_setup.md       # Assign static IPs using nmcli
│   └── requirements.txt       # Python dependencies
├── code/
│   ├── dht_test.py            # Test script for sensor
│   └── mqtt_publish.py        # Send data to MQTT broker/cloud
├── docs/
│   ├── device_list.md         # Static IP plan for all 15 devices
│   └── architecture.png       # System diagram
└── scripts/
    └── static_ip.sh           # Script to assign static IP automatically
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/yousseffwaleed/RaspberryPi-IoT-Project.git
cd RaspberryPi-IoT-Project
```

### 2. Install dependencies
```bash
pip install -r setup/requirements.txt --break-system-packages
```

### 3. Set up the sensor
Follow [Sensor Setup](setup/sensor_setup.md) to:
- Wire the DHT sensor
- Install Python libraries
- Test the sensor with `dht_test.py`

Run the test script:
```bash
python3 code/dht_test.py
```

### 4. Configure static IPs
Follow [Network Setup](setup/network_setup.md) or use the helper script:
```bash
sudo ./scripts/static_ip.sh 1   # Pi 1 → 192.168.0.11
sudo ./scripts/static_ip.sh 2   # Pi 2 → 192.168.0.12
...
sudo ./scripts/static_ip.sh 15  # Pi 15 → 192.168.0.25
```

---

## 📡 Next Steps (coming soon)
- Add and test `mqtt_publish.py` to send sensor data to MQTT broker
- Set up Mosquitto or cloud MQTT (AWS IoT, HiveMQ)
- Automate data publishing with cron/systemd
- Create monitoring dashboard (Grafana/React)
