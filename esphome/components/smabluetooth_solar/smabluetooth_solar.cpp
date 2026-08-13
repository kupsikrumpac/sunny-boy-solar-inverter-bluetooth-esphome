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
#include "esphome/core/log.h"
#include <ctime>

namespace esphome {
namespace smabluetooth_solar {

static const char *const TAG = "smabluetooth_solar";

const StatusCode SmaBluetoothSolar::STATUS_CODES[] = {
    {0x00, "OK"},
    {0x01, "Chyba inicializace Bluetooth"},
    {0x02, "Čekání na spárování"},
    {0x03, "Chyba spárování Bluetooth"},
    {0x04, "Spojení selhalo"},
    {0x05, "Probíhá inicializace SMA"},
    {0x06, "Chyba inicializace SMA"},
    {0x07, "Přihlašování se nezdařilo"},
    {0x08, "Odpojeno / Čekání na obnovení"},
    {0xFFFF, "Neznámý stav"}
};

const char *SmaBluetoothSolar::lookup_code(uint16_t code) {
  for (const auto &item : STATUS_CODES) {
    if (item.code == code) return item.message;
  }
  return STATUS_CODES[sizeof(STATUS_CODES) / sizeof(StatusCode) - 1].message;
}

void SmaBluetoothSolar::setup() {
  ESP_LOGI(TAG, "Inicializace komponenty SMA Bluetooth Solar...");
  this->inverter_state_ = SmaInverterState::Off;
}

void SmaBluetoothSolar::loop() {
  uint32_t now = millis();

  switch (this->inverter_state_) {
    case SmaInverterState::Off:
      if (!this->sma_inverter_) {
        ESP_LOGI(TAG, "Získávám instanci ESP32_SMA_Inverter...");
        this->sma_inverter_ = ESP32_SMA_Inverter::getInstance();
        this->sma_inverter_->setup(
            this->sma_inverter_bluetooth_mac_,
            this->sma_inverter_password_,
            this->sma_inverter_delay_values_
        );
      }
      
      ESP_LOGI(TAG, "Spouštím SMA Bluetooth komunikaci na pozadí...");
      this->sma_inverter_->begin();
      this->inverter_state_ = SmaInverterState::Running;
      break;

    case SmaInverterState::Running:
      if (this->sma_inverter_) {
        // Kontrola, zda nedošlo k vnitřní chybě nebo odpojení střídače
        if (this->sma_inverter_->get_status() == 0x08 || this->sma_inverter_->get_status() == 0x04) {
          if (!this->night_mode_active_) {
            ESP_LOGW(TAG, "Střídač se odpojil (možná nastala noc nebo střídač spí). Vstupuji do úsporného režimu.");
            this->night_mode_active_ = true;
            this->handle_missing_values();
          }
        }
      }
      break;

    case SmaInverterState::Error:
      if (now >= this->error_retry_time_) {
        ESP_LOGI(TAG, "Pokus o opětovné připojení ke střídači...");
        this->inverter_state_ = SmaInverterState::Off;
      }
      break;
  }
}

void SmaBluetoothSolar::handle_missing_values() {
  // Při výpadku nebo noci vynulujeme okamžité hodnoty napětí, proudu a výkonu
  for (size_t i = 0; i < 2; i++) {
    this->update_sensor(this->pvs_[i].voltage_sensor, 0.0f);
    this->update_sensor(this->pvs_[i].current_sensor, 0.0f);
    this->update_sensor(this->pvs_[i].active_power_sensor, 0.0f);
  }
  for (size_t i = 0; i < PHASES; i++) {
    this->update_sensor(this->phases_[i].voltage_sensor, 0.0f);
    this->update_sensor(this->phases_[i].current_sensor, 0.0f);
    this->update_sensor(this->phases_[i].active_power_sensor, 0.0f);
  }
  this->update_sensor(this->grid_relay_binary_sensor_, false);
  this->update_sensor(this->status_text_sensor_, "Odpojeno / Noc");
}

void SmaBluetoothSolar::update() {
  if (!this->sma_inverter_) return;

  uint16_t status = this->sma_inverter_->get_status();
  
  // Publikování stavového textu
  if (this->status_text_sensor_ != nullptr) {
    this->status_text_sensor_->publish_state(this->lookup_code(status));
  }

  // Pokud je střídač spojen a funkční (status 0 = OK)
  if (status == 0x00) {
    if (this->night_mode_active_) {
      ESP_LOGI(TAG, "Střídač se opět probudil a komunikuje!");
      this->night_mode_active_ = false;
    }

    // Načtení a publikace dat
    this->update_sensor(this->today_production_, this->sma_inverter_->get_today_production());
    this->update_sensor(this->total_energy_production_, this->sma_inverter_->get_total_energy_production());
    this->update_sensor(this->grid_frequency_sensor_, this->sma_inverter_->get_grid_frequency());

    // PV Vstupy
    for (size_t i = 0; i < 2; i++) {
      float v = this->sma_inverter_->get_pv_voltage(i);
      float c = this->sma_inverter_->get_pv_current(i);
      
      // Sanitizace neplatných chybových přetečení z SMA
      if (v > 2000.0f) v = 0.0f;
      if (c > 100.0f) c = 0.0f;

      this->update_sensor(this->pvs_[i].voltage_sensor, v);
      this->update_sensor(this->pvs_[i].current_sensor, c);
      this->update_sensor(this->pvs_[i].active_power_sensor, v * c);
    }

    // Fáze
    for (size_t i = 0; i < PHASES; i++) {
      float v = this->sma_inverter_->get_phase_voltage(i);
      float c = this->sma_inverter_->get_phase_current(i);

      if (v > 1000.0f) v = 0.0f;
      if (c > 100.0f) c = 0.0f;

      this->update_sensor(this->phases_[i].voltage_sensor, v);
      this->update_sensor(this->phases_[i].current_sensor, c);
      this->update_sensor(this->phases_[i].active_power_sensor, this->sma_inverter_->get_phase_active_power(i));
    }

    // Relé a teplota
    this->update_sensor(this->grid_relay_binary_sensor_, this->sma_inverter_->get_grid_relay_status());
#if HAVE_MODULE_TEMP
    this->update_sensor(this->inverter_module_temp_, this->sma_inverter_->get_module_temp());
#endif

    // Další informace
    if (this->serial_number_) this->serial_number_->publish_state(this->sma_inverter_->get_serial_number());
    if (this->software_version_) this->software_version_->publish_state(this->sma_inverter_->get_software_version());
    if (this->device_type_) this->device_type_->publish_state(this->sma_inverter_->get_device_type());

  } else {
    // Pokud není ve stavu OK
    if (!this->night_mode_active_) {
      uint32_t now = millis();
      if (now - this->next_night_mode_log_time_ > 300000) { // Log každých 5 minut
        ESP_LOGD(TAG, "Střídač není připraven/komunikace neodpovídá. Stav: 0x%02X", status);
        this->next_night_mode_log_time_ = now;
      }
      this->handle_missing_values();
    }
  }
}

void SmaBluetoothSolar::update_sensor(sensor::Sensor *sensor, float value) {
  if (sensor != nullptr && !std::isnan(value)) {
    sensor->publish_state(value);
  }
}

void SmaBluetoothSolar::update_sensor(text_sensor::TextSensor *sensor, const std::string &value) {
  if (sensor != nullptr) {
    sensor->publish_state(value);
  }
}

void SmaBluetoothSolar::update_sensor(binary_sensor::BinarySensor *sensor, bool value) {
  if (sensor != nullptr) {
    sensor->publish_state(value);
  }
}

void SmaBluetoothSolar::dump_config() {
  ESP_LOGCONFIG(TAG, "SMA Bluetooth Solar Component:");
  ESP_LOGCONFIG(TAG, "  MAC Adresa: %s", this->sma_inverter_bluetooth_mac_.c_str());
  ESP_LOGCONFIG(TAG, "  Povelové prodlení: %" PRIu32 " ms", this->sma_inverter_delay_values_);
}

}  // namespace smabluetooth_solar
}  // namespace esphome
