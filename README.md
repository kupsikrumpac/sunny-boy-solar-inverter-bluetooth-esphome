# SMA Solar Inverter Bluetooth Component for ESPHome

A modernized ESPHome custom component designed to read real-time data from **SMA Sunny Boy** solar inverters via Bluetooth (SMANET2 protocol) using an ESP32 micro-controller.

## 🚀 Features

* **Real-time Monitoring:** Fetch AC/DC voltage, current, power, and frequency.
* **Energy Yield Data:** Today's and total lifetime energy generation statistics.
* **Status Tracking:** Inverter operating mode, grid relay status, and fault lookup messages.
* **ESPHome Native:** Seamless integration with Home Assistant via native API.

---

## 🛠️ Installation & Configuration

Add the repository as an `external_component` in your ESPHome YAML configuration file:

```yaml
external_components:
  - source: github://kupsikrumpac/sunny-boy-solar-inverter-bluetooth-esphome
    components: [ smabluetooth_solar ]

# Core SMA Bluetooth Configuration
smabluetooth_solar:
  mac_address: "00:80:25:XX:XX:XX"  # Replace with your SMA Inverter BT MAC address
  password: "0000"                  # Inverter user password (default is usually 0000)
  update_interval: 10s

# Example Sensor Configuration
sensor:
  - platform: smabluetooth_solar
    today_production:
      name: "SMA Daily Production"
    total_energy_production:
      name: "SMA Total Production"
    grid_frequency:
      name: "SMA Grid Frequency"
    power_dc_1:
      name: "SMA DC Power PV1"
    voltage_dc_1:
      name: "SMA DC Voltage PV1"
    current_dc_1:
      name: "SMA DC Current PV1"
    power_ac_1:
      name: "SMA AC Power Phase 1"
    voltage_ac_1:
      name: "SMA AC Voltage Phase 1"
    current_ac_1:
      name: "SMA AC Current Phase 1"

text_sensor:
  - platform: smabluetooth_solar
    status:
      name: "SMA Inverter Status"
    serial_number:
      name: "SMA Serial Number"
