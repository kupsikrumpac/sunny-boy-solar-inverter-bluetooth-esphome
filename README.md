# SMA Solar Inverter Bluetooth component for ESPHome

Modernizovaná komponenta pro ESPHome umožňující vyčítání dat ze střídačů **SMA Sunny Boy** přes Bluetooth (SMANET2 protocol) pomocí čipu ESP32.

##  Instalace

Přidejte následující blok do vaší ESPHome YAML konfigurace:

```yaml
external_components:
  - source: github://kupsikrumpac/sunny-boy-solar-inverter-bluetooth-esphome
    components: [ smabluetooth_solar ]

# Konfigurace Bluetooth střídače SMA
smabluetooth_solar:
  mac_address: "00:80:25:XX:XX:XX"  # MAC adresa vašeho SMA střídače
  password: "0000"                  # Výchozí uživatelské heslo (obvykle 0000)
  update_interval: 10s

# Příklad senzorů pro Home Assistant
sensor:
  - platform: smabluetooth_solar
    today_production:
      name: "SMA Dnešní výroba"
    total_energy_production:
      name: "SMA Celková výroba"
    grid_frequency:
      name: "SMA Frekvence sítě"
    power_dc_1:
      name: "SMA DC Výkon FVE"
    voltage_dc_1:
      name: "SMA DC Napětí FVE"
    current_dc_1:
      name: "SMA DC Proud FVE"
    power_ac_1:
      name: "SMA AC Výkon do sítě"
    voltage_ac_1:
      name: "SMA AC Napětí"
    current_ac_1:
      name: "SMA AC Proud"

text_sensor:
  - platform: smabluetooth_solar
    status:
      name: "SMA Stav střídače"
    serial_number:
      name: "SMA Sériové číslo"
