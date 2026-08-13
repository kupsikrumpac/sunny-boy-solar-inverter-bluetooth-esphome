/* MIT License

Copyright (c) 2023 keerekeerweere

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Disclaimer
A user of the esphome component software acknowledges that he or she is
receiving this software on an "as is" basis and the user is not relying on
the accuracy or functionality of the software for any purpose. The user further
acknowledges that any use of this software will be at his own risk and the
copyright owner accepts no responsibility whatsoever arising from the use or
application of the software.

SMA, Speedwire are registered trademarks of SMA Solar Technology AG
*/

#pragma once

#ifndef SMABLUETOOTH_SOLAR_H
#define SMABLUETOOTH_SOLAR_H

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "SMA_Inverter.h"

#include <string>
#include <string_view>

#ifndef PHASES
#define PHASES 1  // Default 1 fázový střídač (pro 3f změňte na 3 v nastavení/kódu)
#endif

#ifndef HAVE_MODULE_TEMP
#define HAVE_MODULE_TEMP false
#endif

namespace esphome {
namespace smabluetooth_solar {

enum class SmaBluetoothProtocolVersion {
    SMANET2 = 0
};

enum class SmaInverterState {
    Off,      // BT nevytvořeno
    Running,  // Běží komunikace na pozadí
    Error     // Chyba spojená s časovačem pro opakovaný pokus
};

struct StatusCode {
    uint16_t code;
    const char *message;
};

struct PvInput {
    sensor::Sensor *voltage_sensor{nullptr};
    sensor::Sensor *current_sensor{nullptr};
    sensor::Sensor *active_power_sensor{nullptr};
};

struct Phase {
    sensor::Sensor *voltage_sensor{nullptr};
    sensor::Sensor *current_sensor{nullptr};
    sensor::Sensor *active_power_sensor{nullptr};
};

class SmaBluetoothSolar : public PollingComponent {
 public:
    SmaBluetoothSolar() = default;

    static const StatusCode STATUS_CODES[];

    const char *lookup_code(uint16_t code);
    float get_setup_priority() const override { return setup_priority::LATE; }

    void setup() override;
    void loop() override;
    void update() override;
    void dump_config() override;

    void handle_missing_values();

    // Pomocné metody pro publikaci dat do ESPHome
    void update_sensor(text_sensor::TextSensor *sensor, const std::string &value);
    void update_sensor(sensor::Sensor *sensor, float value);
    void update_sensor(binary_sensor::BinarySensor *sensor, bool value);

    // Konfigurační settery
    void set_protocol_version(SmaBluetoothProtocolVersion v) { protocol_version_ = v; }
    void set_sma_inverter_bluetooth_mac(const std::string &v) { sma_inverter_bluetooth_mac_ = v; }
    void set_sma_inverter_password(const std::string &v) { sma_inverter_password_ = v; }
    void set_sma_inverter_delay_values(uint32_t v) { sma_inverter_delay_values_ = v; }

    // Senzory - Nastavení pointerů
    void set_today_production_sensor(sensor::Sensor *s) { today_production_ = s; }
    void set_total_energy_production_sensor(sensor::Sensor *s) { total_energy_production_ = s; }
    void set_grid_frequency_sensor(sensor::Sensor *s) { grid_frequency_sensor_ = s; }

    void set_pv_voltage_sensor(size_t idx, sensor::Sensor *s) { if (idx < 2) pvs_[idx].voltage_sensor = s; }
    void set_pv_current_sensor(size_t idx, sensor::Sensor *s) { if (idx < 2) pvs_[idx].current_sensor = s; }
    void set_pv_active_power_sensor(size_t idx, sensor::Sensor *s) { if (idx < 2) pvs_[idx].active_power_sensor = s; }

    void set_phase_voltage_sensor(size_t idx, sensor::Sensor *s) { if (idx < PHASES) phases_[idx].voltage_sensor = s; }
    void set_phase_current_sensor(size_t idx, sensor::Sensor *s) { if (idx < PHASES) phases_[idx].current_sensor = s; }
    void set_phase_active_power_sensor(size_t idx, sensor::Sensor *s) { if (idx < PHASES) phases_[idx].active_power_sensor = s; }

    void set_status_text_sensor(text_sensor::TextSensor *s) { status_text_sensor_ = s; }
    void set_grid_relay_binary_sensor(binary_sensor::BinarySensor *s) { grid_relay_binary_sensor_ = s; }
    void set_inverter_module_temp_sensor(sensor::Sensor *s) { inverter_module_temp_ = s; }
    void set_inverter_bluetooth_signal_strength_sensor(sensor::Sensor *s) { inverter_bluetooth_signal_strength_ = s; }

    void set_today_generation_time_sensor(sensor::Sensor *s) { today_generation_time_ = s; }
    void set_total_generation_time_sensor(sensor::Sensor *s) { total_generation_time_ = s; }
    void set_wakeup_time_sensor(sensor::Sensor *s) { wakeup_time_ = s; }

    void set_serial_number_sensor(text_sensor::TextSensor *s) { serial_number_ = s; }
    void set_software_version_sensor(text_sensor::TextSensor *s) { software_version_ = s; }
    void set_device_type_sensor(text_sensor::TextSensor *s) { device_type_ = s; }
    void set_device_class_sensor(text_sensor::TextSensor *s) { device_class_ = s; }
    void set_inverter_time_sensor(text_sensor::TextSensor *s) { inverter_time_sensor_ = s; }

 private:
    ESP32_SMA_Inverter *sma_inverter_{nullptr};

    SmaBluetoothProtocolVersion protocol_version_{SmaBluetoothProtocolVersion::SMANET2};
    std::string sma_inverter_bluetooth_mac_;
    std::string sma_inverter_password_;
    uint32_t sma_inverter_delay_values_{500};

    SmaInverterState inverter_state_{SmaInverterState::Off};
    bool has_setup_{false};
    bool night_mode_active_{false};
    uint32_t next_night_mode_log_time_{0};
    uint32_t error_retry_time_{0};

    // Senzory
    sensor::Sensor *today_production_{nullptr};
    sensor::Sensor *total_energy_production_{nullptr};
    sensor::Sensor *grid_frequency_sensor_{nullptr};

    PvInput pvs_[2];
    Phase phases_[PHASES];

    text_sensor::TextSensor *status_text_sensor_{nullptr};
    binary_sensor::BinarySensor *grid_relay_binary_sensor_{nullptr};
    sensor::Sensor *inverter_module_temp_{nullptr};
    sensor::Sensor *inverter_bluetooth_signal_strength_{nullptr};

    sensor::Sensor *today_generation_time_{nullptr};
    sensor::Sensor *total_generation_time_{nullptr};
    sensor::Sensor *wakeup_time_{nullptr};

    text_sensor::TextSensor *serial_number_{nullptr};
    text_sensor::TextSensor *software_version_{nullptr};
    text_sensor::TextSensor *device_type_{nullptr};
    text_sensor::TextSensor *device_class_{nullptr};
    text_sensor::TextSensor *inverter_time_sensor_{nullptr};
};

}  // namespace smabluetooth_solar
}  // namespace esphome

#endif // SMABLUETOOTH_SOLAR_H
