#!/bin/bash
# static_ip.sh – Assign a static IP to a Raspberry Pi
# Usage: sudo ./static_ip.sh <device_number>
# Example: sudo ./static_ip.sh 7 → assigns 192.168.0.17

SSID="TP-Link_FC93"       # Replace with your Wi-Fi SSID or use "Wired connection 1" if Ethernet
BASE_IP="192.168.0"
START=10                  # Device 1 starts at 192.168.0.11

if [ -z "$1" ]; then
  echo "Usage: sudo $0 <device_number>"
  exit 1
fi

DEVICE_NUM=$1
IP=$((START + DEVICE_NUM))

echo "Assigning static IP $BASE_IP.$IP to device $DEVICE_NUM"

nmcli connection modify "$SSID" ipv4.method manual \
  ipv4.addresses $BASE_IP.$IP/24 \
  ipv4.gateway $BASE_IP.1 \
  ipv4.dns "$BASE_IP.1 8.8.8.8"

nmcli connection down "$SSID"
nmcli connection up "$SSID"

echo "✅ Static IP $BASE_IP.$IP assigned successfully."
