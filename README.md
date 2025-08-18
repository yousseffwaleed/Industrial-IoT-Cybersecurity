# 🌐 Raspberry Pi IoT Project

This project connects **15 Raspberry Pi 5 (8GB)** devices with **DHT11/DHT22 temperature & humidity sensors**, assigns each Pi a **static IP**, and prepares the system to send data to a central **MQTT broker/cloud**.

The goal is to provide a **plug-and-play IoT system** that anyone can set up by following the instructions in this repository.

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
