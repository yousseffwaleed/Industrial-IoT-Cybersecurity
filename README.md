
# ✅ Industrial IoT Testbed Project — Step-by-Step Checklist

This checklist aligns with the `IoT-testbed-setup.pdf` documentation and tracks your implementation of a Raspberry Pi-based critical infrastructure simulation.

---

## ✅ Phase 1: Core Device Setup (Completed)
| Task | Status |
|------|--------|
| Assign static IPs to 15 Raspberry Pis | ✅ Done |
| SSH access to all Raspberry Pis | ✅ Done |
| Install Python libraries (DHT, MQTT) on Pis | ✅ Done |
| Test DHT11 sensors and get data | ✅ Done |
| Run `mqtt_publish.py` and verify data via Jetson MQTT subscriber | ✅ Done |

---

## 🚦 Phase 2: Cluster Mapping and Topic Setup
| Task | Description |
|------|-------------|
| 📌 **Map Raspberry Pis to clusters** | Assign Pis to:<br> - Cluster 1: Control Room Devices<br> - Cluster 2: Field Sensor Network<br> - Cluster 3: Human Monitoring |
| 🛠 **Update MQTT topic structure** | Update topic in each `mqtt_publish.py`:<br>`iot/clusterX/piYY` |
| 📁 **Document device mapping** | Update `docs/device_list.md` with IP, cluster, role |

---

## 🧠 Phase 3: MQTT Broker + Data Aggregation
| Task | Description |
|------|-------------|
| 🧩 **Install Mosquitto MQTT broker** | Choose 1 device as broker:<br>`sudo apt install mosquitto mosquitto-clients -y` |
| 📬 **Redirect publishers to broker** | Update `broker_ip = "192.168.0.X"` in each Pi’s script |
| 📈 **Test subscriber on Jetson** | Run:<br>`mosquitto_sub -t "iot/#" -v` and verify messages |

---

## 🖥️ Phase 4: Central Logging + Flask Server (Pi-3)
| Task | Description |
|------|-------------|
| 🧪 **Create Flask logging endpoint** | Host Flask app to accept sensor data (HTTP POST) |
| 📄 **Log to CSV or SQLite** | Log MQTT or HTTP payloads by timestamp/device |
| 📊 **Optional: Add visualization** | Use `matplotlib`, Grafana, or Node-RED |

---

## 🔐 Phase 5: Traffic Monitoring + Attack Simulation
| Task | Description |
|------|-------------|
| 🔍 **Install Zeek, tcpdump, Suricata** | On Jetson or Pi: monitor and capture traffic |
| 🧨 **Simulate IoT attacks** | Modify publisher scripts to simulate:<br> - Spikes<br> - Flooding<br> - Fake vitals |
| 📉 **Analyze traffic** | Use Wireshark/Zeek logs to detect anomalies |

---

## 🧩 Optional Advanced Add-Ons
| Feature | Devices |
|---------|---------|
| Smart Bulbs (spoof blinking) | Pi GPIO / Relay |
| RFID Reader (fake access) | USB RFID log trigger |
| ESP32-CAM (video spoof) | Camera stream fake |
| Smartwatch spoofing | Simulated MQTT from health sensors |

---

## ✅ Final Step: Documentation & Automation
| Task | Description |
|------|-------------|
| 📘 **Update README.md** | Add diagrams, instructions, topic structure |
| 🔁 **Auto-start scripts** | Use `crontab` or `systemd` |
| 📎 **Log test runs** | Save screenshots, logs, and analysis |
