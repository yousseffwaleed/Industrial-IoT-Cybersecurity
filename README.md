# 🌐 Raspberry Pi IoT Network  
**A scalable IoT system using 15 Raspberry Pi 5 devices with DHT11/DHT22 sensors, static IPs, and MQTT integration.**  


---

## 📌 Key Features  
- ✅ **Real-time sensor data** (temperature & humidity) from 15 nodes  
- ✅ **Automated static IP assignment** (script for all 15 Pis)  
- ✅ **Pre-configured test scripts** (`dht_test.py`)  
- 🔄 **Future:** MQTT pipeline to cloud/broker (Mosquitto/AWS IoT)  
- 📖 **Complete documentation** for easy replication  

---

## 🛠️ Hardware Requirements  
| Component              | Quantity | Notes                          |  
|------------------------|----------|--------------------------------|  
| Raspberry Pi 5 (8GB)   | 15       | Static IP configured           |  
| DHT11/DHT22 Sensors    | 15       | `Adafruit_DHT` compatible      |  
| MicroSD Cards (32GB+)  | 15       | Raspberry Pi OS Lite (64-bit)  |  
| Network Switch         | 1        | Supports static IP leasing     |  
| Jumper Wires           | 45       | 3 per sensor (VCC/GND/Data)    |  

---

## 📂 Repository Structure  
```plaintext
RaspberryPi-IoT-Project/
├── setup/
│   ├── sensor_setup.md     # Wiring + library guide
│   ├── network_setup.md    # Static IP configuration
│   └── requirements.txt    # Python dependencies
├── code/
│   ├── dht_test.py         # Sensor validation
│   └── mqtt_publish.py     # (Future) MQTT client
├── scripts/
│   └── static_ip.sh        # Auto-IP (Pi 1 → 192.168.0.11)
└── docs/
    ├── device_list.md      # IP allocation table
    └── architecture.png    # System diagram



🚀 Quick Start

1. Initial Setup

bash
git clone https://github.com/yousseffwaleed/RaspberryPi-IoT-Project.git
cd RaspberryPi-IoT-Project
sudo apt update && sudo apt install python3-pip
pip3 install -r setup/requirements.txt
2. Sensor Configuration

Wire sensors:
VCC → 3.3V (Pin 1)
DATA → GPIO4 (Pin 7)
GND → Ground (Pin 6)
Test:
bash
python3 code/dht_test.py
