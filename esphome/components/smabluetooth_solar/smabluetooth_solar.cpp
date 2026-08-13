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

#include "smabluetooth_solar.h"
#include "esphome/core/application.h"
#include "esphome/core/hal.h"
#include "esphome/core/log.h"

namespace esphome {
namespace smabluetooth_solar {

static const char *const TAG = "smabluetooth_solar";

// Prehlednejsi mapovani stavovych kodu
const StatusCode SmaBluetoothSolar::STATUS_CODES[] = {
    {50,   "Status"},
    {51,   "Closed"},
    {300,  "Nat"},
    {301,  "Grid failure"},
    {302,  "-------"},
    {303,  "Off"},
    {304,  "Island mode"},
    {305,  "Island mode"},
    {306,  "SMA Island mode 60 Hz"},
    {307,  "OK"},
    {308,  "On"},
    {309,  "Operation"},
    {310,  "General operating mode"},
    {311,  "Open"},
    {312,  "Phase assignment"},
    {313,  "SMA Island mode 50 Hz"},
    {358,  "SB 4000TL-20"},
    {359,  "SB 5000TL-20"},
    {558,  "SB 3000TL-20"},
    {6109, "SB 1600TL-10"},
    {9109, "SB 1600TL-10"},
    {8001, "Solar Inverters"},
    {71,   "Interference device"},
    {73,   "Diffuse insolation"},
    {74,   "Direct insolation"},
    {76,   "Fault correction measure"},
    {77,   "Check AC circuit breaker"},
    {78,   "Check generator"},
    {79,   "Disconnect generator"},
    {80,   "Check parameter"},
    {84,   "Overcurrent GRID hw"},
    {85,   "Overcurrent GRID sw"},
    {87,   "GRID frequency disturbance"},
    {88,   "GRID frequency not permitted"},
    {89,   "GRID disconnection point"}
};

void SmaBluetoothSolar::setup() {
    ESP_LOGCONFIG(TAG, "Inicializace SMA Bluetooth Solar...");
    sma_inverter_ = ESP32_SMA_Inverter::getInstance();
    sma_inverter_->setup(sma_inverter_bluetooth_mac_,
                        sma_inverter_password_,
                        sma_inverter_delay_values_);
    has_setup_ = true;
    ESP_LOGI(TAG, "Setup dokončen pro střídač MAC: %s", sma_inverter_bluetooth_mac_.c_str());
}

void SmaBluetoothSolar::loop() {
    App.feed_wdt();

    if (!has_setup_) return;

    const uint32_t now = millis();

    switch (inverter_state_) {
        case SmaInverterState::Off:
            if (sma_inverter_->begin("ESP32toSMA")) {
                sma_inverter_->startBtTask();
                inverter_state_ = SmaInverterState::Running;
                ESP_LOGI(TAG, "Bluetooth úloha spuštěna (Stav -> Running)");
            } else {
                ESP_LOGE(TAG, "Bluetooth begin selhal. Opakovaný pokus za 10s");
                error_retry_time_ = now + 10000;
                inverter_state_ = SmaInverterState::Error;
            }
            break;

        case SmaInverterState::Running:
            if (sma_inverter_->isNightModeActive()) {
                if (!night_mode_active_ || now >= next_night_mode_log_time_) {
                    ESP_LOGI(TAG, "Noční režim aktivní: Dotazování pozastaveno.");
                    night_mode_active_ = true;
                    next_night_mode_log_time_ = now + 60000;
                }
            } else if (night_mode_active_) {
                ESP_LOGI(TAG, "Noční režim ukončen: Dotazování obnoveno.");
                night_mode_active_ = false;
                next_night_mode_log_time_ = 0;
            }

            if (sma_inverter_->hasTaskError()) {
                ESP_LOGE(TAG, "Detekována chyba Bluetooth tasku! Restart za 10s...");
                sma_inverter_->clearTaskError();
                sma_inverter_->stopBtTask();
                error_retry_time_ = now + 10000;
                inverter_state_ = SmaInverterState::Error;
            }
            break;

        case SmaInverterState::Error:
            if (now >= error_retry_time_) {
                ESP_LOGI(TAG, "Restartuji Bluetooth task...");
                sma_inverter_->startBtTask();
                inverter_state_ = SmaInverterState::Running;
            }
            break;
    }
}

void SmaBluetoothSolar::update() {
    if (!sma_inverter_) return;

    handle_missing_values();

    // Výkon a frekvence
    update_sensor(today_production_,         sma_inverter_->dispData.EToday);
    update_sensor(total_energy_production_,  sma_inverter_->dispData.ETotal);
    update_sensor(grid_frequency_sensor_,    sma_inverter_->dispData.GridFreq);

    // PV Vstupy
    update_sensor(pvs_[0].voltage_sensor,      sma_inverter_->dispData.Udc1);
    update_sensor(pvs_[0].current_sensor,      sma_inverter_->dispData.Idc1);
    update_sensor(pvs_[0].active_power_sensor, sma_inverter_->dispData.Pdc1);

    update_sensor(pvs_[1].voltage_sensor,      sma_inverter_->dispData.Udc2);
    update_sensor(pvs_[1].current_sensor,      sma_inverter_->dispData.Idc2);
    update_sensor(pvs_[1].active_power_sensor, sma_inverter_->dispData.Pdc2);

    // AC Fáze
    update_sensor(phases_[0].voltage_sensor,      sma_inverter_->dispData.Uac1);
    update_sensor(phases_[0].current_sensor,      sma_inverter_->dispData.Iac1);
    update_sensor(phases_[0].active_power_sensor, sma_inverter_->dispData.Pac1);

#if PHASES > 1
    update_sensor(phases_[1].voltage_sensor,      sma_inverter_->dispData.Uac2);
    update_sensor(phases_[1].current_sensor,      sma_inverter_->dispData.Iac2);
    update_sensor(phases_[1].active_power_sensor, sma_inverter_->dispData.Pac2);
#endif

#if PHASES > 2
    update_sensor(phases_[2].voltage_sensor,      sma_inverter_->dispData.Uac3);
    update_sensor(phases_[2].current_sensor,      sma_inverter_->dispData.Iac3);
    update_sensor(phases_[2].active_power_sensor, sma_inverter_->dispData.Pac3);
#endif

    // Stavové senzory
    update_sensor(status_text_sensor_, lookup_code(sma_inverter_->invData.DevStatus));
    update_sensor(grid_relay_binary_sensor_, sma_inverter_->invData.GridRelay == 51); // 51 = Closed

#if HAVE_MODULE_TEMP
    update_sensor(inverter_module_temp_, sma_inverter_->dispData.InvTemp);
#endif

    update_sensor(inverter_bluetooth_signal_strength_, sma_inverter_->dispData.BTSigStrength);
    update_sensor(today_generation_time_, static_cast<float>(sma_inverter_->invData.OperationTime) / 3600.0f);
    update_sensor(total_generation_time_, static_cast<float>(sma_inverter_->invData.FeedInTime) / 3600.0f);
    update_sensor(wakeup_time_, static_cast<float>(sma_inverter_->invData.WakeupTime));
    
    update_sensor(serial_number_, sma_inverter_->invData.DeviceName);
    update_sensor(software_version_, sma_inverter_->invData.SWVersion);
    update_sensor(device_type_, lookup_code(sma_inverter_->invData.DeviceType));
    update_sensor(device_class_, lookup_code(sma_inverter_->invData.DeviceClass));
    update_sensor(inverter_time_sensor_, sma_inverter_->invData.InverterTimestamp);

    sma_inverter_->clearDataReady();
}

void SmaBluetoothSolar::handle_missing_values() {
    auto &d = sma_inverter_->dispData;

    if (d.Pdc1 == 0.0f || d.needsMissingValues) {
        if (d.Udc1 != 0.0f && d.Idc1 != 0.0f) {
            d.Pdc1 = (d.Udc1 * d.Idc1) / 1000.0f;
            d.needsMissingValues = true;
        }
    }
    if (d.Pdc2 == 0.0f || d.needsMissingValues) {
        if (d.Udc2 != 0.0f && d.Idc2 != 0.0f) {
            d.Pdc2 = (d.Udc2 * d.Idc2) / 1000.0f;
            d.needsMissingValues = true;
        }
    }
    if (d.Pac1 == 0.0f || d.needsMissingValues) {
        if (d.Uac1 != 0.0f && d.Iac1 != 0.0f) {
            d.Pac1 = (d.Uac1 * d.Iac1) / 1000.0f;
            d.needsMissingValues = true;
        }
    }
#if PHASES > 1
    if (d.Pac2 == 0.0f || d.needsMissingValues) {
        if (d.Uac2 != 0.0f && d.Iac2 != 0.0f) {
            d.Pac2 = (d.Uac2 * d.Iac2) / 1000.0f;
            d.needsMissingValues = true;
        }
    }
#endif
#if PHASES > 2
    if (d.Pac3 == 0.0f || d.needsMissingValues) {
        if (d.Uac3 != 0.0f && d.Iac3 != 0.0f) {
            d.Pac3 = (d.Uac3 * d.Iac3) / 1000.0f;
            d.needsMissingValues = true;
        }
    }
#endif
}

// Bezpečné pomocné funkce s kontrolou nullptr
void SmaBluetoothSolar::update_sensor(text_sensor::TextSensor *sensor, const std::string &value) {
    if (sensor != nullptr && !value.empty()) {
        sensor->publish_state(value);
    }
}

void SmaBluetoothSolar::update_sensor(sensor::Sensor *sensor, float value) {
    if (sensor != nullptr && value >= 0.0f) {
        sensor->publish_state(value);
    }
}

void SmaBluetoothSolar::update_sensor(binary_sensor::BinarySensor *sensor, bool value) {
    if (sensor != nullptr) {
        sensor->publish_state(value);
    }
}

void SmaBluetoothSolar::dump_config() {
    ESP_LOGCONFIG(TAG, "SMA Bluetooth Solar Komponenta:");
    ESP_LOGCONFIG(TAG, "  MAC adresa: %s", sma_inverter_bluetooth_mac_.c_str());
    ESP_LOGCONFIG(TAG, "  Prodleva dotazování: %u ms", sma_inverter_delay_values_);
}

const char *SmaBluetoothSolar::lookup_code(uint16_t code) {
    for (const auto &entry : STATUS_CODES) {
        if (entry.code == code) return entry.message;
    }
    return "Neznámý stav";
}

}  // namespace smabluetooth_solar
}  // namespace esphome