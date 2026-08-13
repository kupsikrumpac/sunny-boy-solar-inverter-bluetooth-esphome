# Repository Guidelines

## Project Structure & Module Organization
This repository is an ESPHome external component for SMA inverters over classic Bluetooth. Core component code lives in `esphome/components/smabluetooth_solar/`: C++ runtime logic is in `smabluetooth_solar.cpp`, `smabluetooth_solar.h`, `SMA_Inverter.cpp`, and `SMA_Inverter.h`; the ESPHome config schema is in `sensor.py`. Sample configuration and helper scripts live in `esphome/sample/`, including `smabluesolar.yaml` and `generate-partitions.py`. Keep new component files under the existing `smabluetooth_solar` namespace.

## Hardware Constraints

- Targets **ESP-IDF** framework (not Arduino). Agents may default to Arduino; always verify `framework:` in YAML matches `type: esp-idf`.
- Only standard **ESP32** supports classic Bluetooth (SPP). ESP32-S2/S3/C2/C3/C5/C6/C61 are incompatible. WROVER/U/D/S flash variants all work.
- BLE is disabled (`CONFIG_BT_BLE_ENABLED: n`) because classic BT SPP shares Bluedroid resources — enabling both causes runtime crashes.

## Build, Test, and Development Commands
Use ESPHome from the repository root.

- `esphome config esphome/sample/smabluesolar.yaml` validates YAML and Python schema wiring.
- `esphome compile esphome/sample/smabluesolar.yaml` builds the sample node and catches C++ integration errors.
- `esphome run esphome/sample/smabluesolar.yaml` flashes a test device when hardware is available.
- `python3 esphome/sample/generate-partitions.py` prints a partition table for ESP32 sizing checks.

For local development, point `external_components` in the sample YAML at a local path instead of the GitHub URL.

## Coding Style & Naming Conventions
Follow the existing style in each language. Python uses 4-space indentation, `snake_case` keys, and `UPPER_SNAKE_CASE` constants for config names. C++ uses the ESPHome pattern: `PascalCase` classes, `snake_case_` member fields with trailing underscores, and concise logging via `ESP_LOG*`. Keep YAML option names lowercase with underscores, for example `sma_inverter_bluetooth_mac`.

## Testing Guidelines
No test suite exists — `esphome config` + `esphome compile` is the full verification loop; run both after every change. When modifying inverter communication or sensor mapping, test against real ESP32 hardware and note the inverter model (e.g., `SB3000TL-20`, `SB1600TL-10`). Keep `smabluesolar.yaml` up-to-date when config options change — it doubles as documentation and regression fixture.

## Commit & Pull Request Guidelines
Recent history uses short, imperative subjects such as `fix compile`, `buffer`, and `review type label`. Keep commit titles brief, present tense, and focused on one change. Pull requests should describe the user-visible impact, list the ESPHome commands run, and mention any hardware verification performed. Include updated YAML snippets or logs when changing configuration shape or Bluetooth behavior.
