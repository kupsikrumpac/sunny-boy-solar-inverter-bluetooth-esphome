import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, sensor, text_sensor
from esphome.const import (
    CONF_ACTIVE_POWER,
    CONF_CURRENT,
    CONF_FREQUENCY,
    CONF_ID,
    CONF_MAC_ADDRESS,
    CONF_PASSWORD,
    CONF_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_TIMESTAMP,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_CELSIUS,
    UNIT_HERTZ,
    UNIT_HOUR,
    UNIT_KILOWATT_HOURS,
    UNIT_PERCENT,
    UNIT_VOLT,
    UNIT_WATT,
)
from esphome.core import CORE

AUTO_LOAD = ["sensor", "text_sensor", "binary_sensor"]

smabluetooth_solar_ns = cg.esphome_ns.namespace("smabluetooth_solar")
SmaBluetoothSolar = smabluetooth_solar_ns.class_(
    "SmaBluetoothSolar", cg.PollingComponent
)

# Konfigurační klíče pro kompatibilitu obou zápisů
CONF_SMA_INVERTER_BLUETOOTH_MAC = "sma_inverter_bluetooth_mac"
CONF_SMA_INVERTER_PASSWORD = "sma_inverter_password"
CONF_SMA_INVERTER_DELAY_VALUES = "sma_inverter_delay_values"
CONF_SMA_INVERTER_NIGHT_MARGIN = "sma_inverter_night_margin"
CONF_PROTOCOL_VERSION = "protocol_version"

# AC a DC Klíče
CONF_PHASE_A = "phase_a"
CONF_PHASE_B = "phase_b"
CONF_PHASE_C = "phase_c"
CONF_PV1 = "pv1"
CONF_PV2 = "pv2"
CONF_POWER_DC_1 = "power_dc_1"
CONF_VOLTAGE_DC_1 = "voltage_dc_1"
CONF_CURRENT_DC_1 = "current_dc_1"
CONF_POWER_AC_1 = "power_ac_1"
CONF_VOLTAGE_AC_1 = "voltage_ac_1"
CONF_CURRENT_AC_1 = "current_ac_1"

# Senzory energie a statistik
CONF_ENERGY_PRODUCTION_DAY = "energy_production_day"
CONF_TODAY_PRODUCTION = "today_production"
CONF_TOTAL_ENERGY_PRODUCTION = "total_energy_production"
CONF_GRID_FREQUENCY = "grid_frequency"
CONF_INVERTER_MODULE_TEMP = "inverter_module_temp"
CONF_TODAY_GENERATION_TIME = "today_generation_time"
CONF_TOTAL_GENERATION_TIME = "total_generation_time"
CONF_WAKEUP_TIME = "wakeup_time"
CONF_SMA_INVERTER_BLUETOOTH_SIGNAL_STRENGTH = "sma_inverter_bluetooth_signal_strength"

# Textové a Binární senzory
CONF_STATUS = "status"
CONF_INVERTER_STATUS = "inverter_status"
CONF_SERIAL_NUMBER = "serial_number"
CONF_SOFTWARE_VERSION = "software_version"
CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_CLASS = "device_class"
CONF_INVERTER_TIME = "inverter_time"
CONF_GRID_RELAY = "grid_relay"

# Schémata pro fáze a PV vstupy
PHASE_SCHEMA = cv.Schema(
    {
        cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_CURRENT): sensor.sensor_schema(
            unit_of_measurement=UNIT_AMPERE,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_CURRENT,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_ACTIVE_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_WATT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
    }
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(SmaBluetoothSolar),
            cv.Optional(CONF_MAC_ADDRESS): cv.mac_address,
            cv.Optional(CONF_SMA_INVERTER_BLUETOOTH_MAC): cv.mac_address,
            cv.Optional(CONF_PASSWORD, default="0000"): cv.string,
            cv.Optional(CONF_SMA_INVERTER_PASSWORD, default="0000"): cv.string,
            cv.Optional(CONF_SMA_INVERTER_DELAY_VALUES, default="200ms"): cv.positive_time_period_milliseconds,
            cv.Optional(CONF_SMA_INVERTER_NIGHT_MARGIN, default="30min"): cv.positive_time_period_milliseconds,
            
            # Vnořené fáze i přímé senzory
            cv.Optional(CONF_PHASE_A): PHASE_SCHEMA,
            cv.Optional(CONF_PHASE_B): PHASE_SCHEMA,
            cv.Optional(CONF_PHASE_C): PHASE_SCHEMA,
            cv.Optional(CONF_PV1): PHASE_SCHEMA,
            cv.Optional(CONF_PV2): PHASE_SCHEMA,

            cv.Optional(CONF_POWER_DC_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_VOLTAGE_DC_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_DC_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_POWER_AC_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_WATT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_POWER,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_VOLTAGE_AC_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CURRENT_AC_1): sensor.sensor_schema(
                unit_of_measurement=UNIT_AMPERE,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_CURRENT,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            
            # Statistiky a Čísla
            cv.Optional(CONF_ENERGY_PRODUCTION_DAY): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TODAY_PRODUCTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TOTAL_ENERGY_PRODUCTION): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOWATT_HOURS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_ENERGY,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_GRID_FREQUENCY): sensor.sensor_schema(
                unit_of_measurement=UNIT_HERTZ,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_FREQUENCY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_CONF_FREQUENCY): sensor.sensor_schema(
                unit_of_measurement=UNIT_HERTZ,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_FREQUENCY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_INVERTER_MODULE_TEMP): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_TODAY_GENERATION_TIME): sensor.sensor_schema(
                unit_of_measurement=UNIT_HOUR,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_TOTAL_GENERATION_TIME): sensor.sensor_schema(
                unit_of_measurement=UNIT_HOUR,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_DURATION,
                state_class=STATE_CLASS_TOTAL_INCREASING,
            ),
            cv.Optional(CONF_SMA_INVERTER_BLUETOOTH_SIGNAL_STRENGTH): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
                state_class=STATE_CLASS_MEASUREMENT,
            ),

            # Textové senzory
            cv.Optional(CONF_STATUS): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_INVERTER_STATUS): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_SERIAL_NUMBER): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_SOFTWARE_VERSION): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_DEVICE_TYPE): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_DEVICE_CLASS): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_INVERTER_TIME): text_sensor.text_sensor_schema(),

            # Binární senzor relé
            cv.Optional(CONF_GRID_RELAY): binary_sensor.binary_sensor_schema(),
        }
    )
    .extend(cv.polling_component_schema("10s"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    # MAC adresa a Heslo (zpracování obou verzí zápisu)
    mac = config.get(CONF_SMA_INVERTER_BLUETOOTH_MAC) or config.get(CONF_MAC_ADDRESS)
    if mac:
        cg.add(var.set_sma_inverter_bluetooth_mac(str(mac)))

    pwd = config.get(CONF_SMA_INVERTER_PASSWORD) or config.get(CONF_PASSWORD)
    if pwd:
        cg.add(var.set_sma_inverter_password(str(pwd)))

    # Vyčítání vnořených fází (phase_a, phase_b, phase_c)
    for i, phase in enumerate([CONF_PHASE_A, CONF_PHASE_B, CONF_PHASE_C]):
        if phase in config:
            p_cfg = config[phase]
            if CONF_VOLTAGE in p_cfg:
                sens = await sensor.new_sensor(p_cfg[CONF_VOLTAGE])
                cg.add(var.set_voltage_sensor(i, sens))
            if CONF_CURRENT in p_cfg:
                sens = await sensor.new_sensor(p_cfg[CONF_CURRENT])
                cg.add(var.set_current_sensor(i, sens))
            if CONF_ACTIVE_POWER in p_cfg:
                sens = await sensor.new_sensor(p_cfg[CONF_ACTIVE_POWER])
                cg.add(var.set_active_power_sensor(i, sens))

    # Vyčítání vnořených PV vstupů (pv1, pv2)
    for i, pv in enumerate([CONF_PV1, CONF_PV2]):
        if pv in config:
            pv_cfg = config[pv]
            if CONF_VOLTAGE in pv_cfg:
                sens = await sensor.new_sensor(pv_cfg[CONF_VOLTAGE])
                cg.add(var.set_voltage_sensor_pv(i, sens))
            if CONF_CURRENT in pv_cfg:
                sens = await sensor.new_sensor(pv_cfg[CONF_CURRENT])
                cg.add(var.set_current_sensor_pv(i, sens))
            if CONF_ACTIVE_POWER in pv_cfg:
                sens = await sensor.new_sensor(pv_cfg[CONF_ACTIVE_POWER])
                cg.add(var.set_active_power_sensor_pv(i, sens))

    # Ploché senzory DC1 a AC1
    if CONF_POWER_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_POWER_DC_1])
        cg.add(var.set_active_power_sensor_pv(0, sens))
    if CONF_VOLTAGE_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_VOLTAGE_DC_1])
        cg.add(var.set_voltage_sensor_pv(0, sens))
    if CONF_CURRENT_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_DC_1])
        cg.add(var.set_current_sensor_pv(0, sens))

    if CONF_POWER_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_POWER_AC_1])
        cg.add(var.set_active_power_sensor(0, sens))
    if CONF_VOLTAGE_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_VOLTAGE_AC_1])
        cg.add(var.set_voltage_sensor(0, sens))
    if CONF_CURRENT_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_AC_1])
        cg.add(var.set_current_sensor(0, sens))

    # Statistiky výroby
    today_sens = config.get(CONF_TODAY_PRODUCTION) or config.get(CONF_ENERGY_PRODUCTION_DAY)
    if today_sens:
        sens = await sensor.new_sensor(today_sens)
        cg.add(var.set_today_production_sensor(sens))

    if CONF_TOTAL_ENERGY_PRODUCTION in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ENERGY_PRODUCTION])
        cg.add(var.set_total_energy_production_sensor(sens))

    freq_sens = config.get(CONF_GRID_FREQUENCY) or config.get(CONF_FREQUENCY)
    if freq_sens:
        sens = await sensor.new_sensor(freq_sens)
        cg.add(var.set_grid_frequency_sensor(sens))

    if CONF_INVERTER_MODULE_TEMP in config:
        sens = await sensor.new_sensor(config[CONF_INVERTER_MODULE_TEMP])
        cg.add(var.set_inverter_module_temp_sensor(sens))

    if CONF_TODAY_GENERATION_TIME in config:
        sens = await sensor.new_sensor(config[CONF_TODAY_GENERATION_TIME])
        cg.add(var.set_today_generation_time(sens))

    if CONF_TOTAL_GENERATION_TIME in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_GENERATION_TIME])
        cg.add(var.set_total_generation_time(sens))

    if CONF_SMA_INVERTER_BLUETOOTH_SIGNAL_STRENGTH in config:
        sens = await sensor.new_sensor(config[CONF_SMA_INVERTER_BLUETOOTH_SIGNAL_STRENGTH])
        cg.add(var.set_inverter_bluetooth_signal_strength(sens))

    # Textové senzory
    status_sens = config.get(CONF_STATUS) or config.get(CONF_INVERTER_STATUS)
    if status_sens:
        sens = await text_sensor.new_text_sensor(status_sens)
        cg.add(var.set_inverter_status_sensor(sens))

    if CONF_SERIAL_NUMBER in config:
        sens = await text_sensor.new_text_sensor(config[CONF_SERIAL_NUMBER])
        cg.add(var.set_serial_number(sens))

    if CONF_SOFTWARE_VERSION in config:
        sens = await text_sensor.new_text_sensor(config[CONF_SOFTWARE_VERSION])
        cg.add(var.set_software_version(sens))

    if CONF_DEVICE_TYPE in config:
        sens = await text_sensor.new_text_sensor(config[CONF_DEVICE_TYPE])
        cg.add(var.set_device_type(sens))

    if CONF_DEVICE_CLASS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_DEVICE_CLASS])
        cg.add(var.set_device_class(sens))

    if CONF_INVERTER_TIME in config:
        sens = await text_sensor.new_text_sensor(config[CONF_INVERTER_TIME])
        cg.add(var.set_inverter_time_sensor(sens))

    # Binární senzor
    if CONF_GRID_RELAY in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_GRID_RELAY])
        cg.add(var.set_grid_relay_sensor(sens))

    if CORE.using_arduino and (CORE.is_esp32 or CORE.is_esp8266):
        cg.add_library("BluetoothSerial", None)
