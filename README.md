# 🌐 Raspberry Pi IoT Network  
**A scalable IoT system using 15 Raspberry Pi 5 devices with DHT11/DHT22 sensors, static IPs, and MQTT integration.**  


---

## 📌 Key Features  
- ✅ **Real-time sensor data** (temperature & humidity) from 15 nodes.  
- ✅ **Automated static IP assignment** (script included for all 15 Pis).  
- ✅ **Pre-configured scripts** for sensor testing (`dht_test.py`).  
- 🔄 **Future:** MQTT data pipeline to cloud/broker (e.g., Mosquitto, AWS IoT).  
- 📖 **Full documentation** for easy replication.  

---

## 🛠️ Hardware Requirements  
| Component              | Quantity | Notes                          |  
|------------------------|----------|--------------------------------|  
| Raspberry Pi 5 (8GB)   | 15       | Configured with static IPs.    |  
| DHT11/DHT22 Sensors    | 15       | Tested with `Adafruit_DHT` lib.|  
| MicroSD Cards (32GB+)  | 15       | OS: Raspberry Pi OS Lite (64-bit). |  
| Network Switch/Router  | 1        | Must support static IP leasing. |  

---

## 📂 Repository Structure  
