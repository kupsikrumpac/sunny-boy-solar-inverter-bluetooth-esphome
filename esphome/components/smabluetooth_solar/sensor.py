import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, text_sensor, binary_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    DEVICE_CLASS_TEMPERATURE,
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

from . import SmaBluetoothSolar, smabluetooth_solar_ns

CONF_SMA_BLUETOOTH_SOLAR_ID = "smabluetooth_solar_id"

# AC a DC Klíče
CONF_POWER_AC_1 = "power_ac_1"
CONF_VOLTAGE_AC_1 = "voltage_ac_1"
CONF_CURRENT_AC_1 = "current_ac_1"

CONF_POWER_DC_1 = "power_dc_1"
CONF_VOLTAGE_DC_1 = "voltage_dc_1"
CONF_CURRENT_DC_1 = "current_dc_1"

# Statistiky
CONF_TODAY_PRODUCTION = "today_production"
CONF_TOTAL_ENERGY_PRODUCTION = "total_energy_production"
CONF_GRID_FREQUENCY = "grid_frequency"
CONF_INVERTER_MODULE_TEMP = "inverter_module_temp"
CONF_TODAY_GENERATION_TIME = "today_generation_time"
CONF_TOTAL_GENERATION_TIME = "total_generation_time"
CONF_SIGNAL_STRENGTH = "sma_inverter_bluetooth_signal_strength"

# Textové a Binární
CONF_STATUS = "status"
CONF_SERIAL_NUMBER = "serial_number"
CONF_SOFTWARE_VERSION = "software_version"
CONF_DEVICE_TYPE = "device_type"
CONF_INVERTER_TIME = "inverter_time"
CONF_GRID_RELAY = "grid_relay"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_SMA_BLUETOOTH_SOLAR_ID): cv.use_id(SmaBluetoothSolar),
        
        # AC
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

        # DC
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

        # Statistiky
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
        cv.Optional(CONF_SIGNAL_STRENGTH): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
            state_class=STATE_CLASS_MEASUREMENT,
        ),

        # Textové
        cv.Optional(CONF_STATUS): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_SERIAL_NUMBER): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_SOFTWARE_VERSION): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_DEVICE_TYPE): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_INVERTER_TIME): text_sensor.text_sensor_schema(),

        # Binární
        cv.Optional(CONF_GRID_RELAY): binary_sensor.binary_sensor_schema(),
    }
)


async def to_code(config):
    hub = await cg.get_variable(config[CONF_SMA_BLUETOOTH_SOLAR_ID])

    # AC
    if CONF_POWER_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_POWER_AC_1])
        cg.add(hub.set_active_power_sensor(0, sens))
    if CONF_VOLTAGE_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_VOLTAGE_AC_1])
        cg.add(hub.set_voltage_sensor(0, sens))
    if CONF_CURRENT_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_AC_1])
        cg.add(hub.set_current_sensor(0, sens))

    # DC
    if CONF_POWER_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_POWER_DC_1])
        cg.add(hub.set_active_power_sensor_pv(0, sens))
    if CONF_VOLTAGE_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_VOLTAGE_DC_1])
        cg.add(hub.set_voltage_sensor_pv(0, sens))
    if CONF_CURRENT_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_DC_1])
        cg.add(hub.set_current_sensor_pv(0, sens))

    # Statistiky
    if CONF_TODAY_PRODUCTION in config:
        sens = await sensor.new_sensor(config[CONF_TODAY_PRODUCTION])
        cg.add(hub.set_today_production_sensor(sens))
    if CONF_TOTAL_ENERGY_PRODUCTION in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ENERGY_PRODUCTION])
        cg.add(hub.set_total_energy_production_sensor(sens))
    if CONF_GRID_FREQUENCY in config:
        sens = await sensor.new_sensor(config[CONF_GRID_FREQUENCY])
        cg.add(hub.set_grid_frequency_sensor(sens))
    if CONF_INVERTER_MODULE_TEMP in config:
        sens = await sensor.new_sensor(config[CONF_INVERTER_MODULE_TEMP])
        cg.add(hub.set_inverter_module_temp_sensor(sens))
    if CONF_TODAY_GENERATION_TIME in config:
        sens = await sensor.new_sensor(config[CONF_TODAY_GENERATION_TIME])
        cg.add(hub.set_today_generation_time(sens))
    if CONF_TOTAL_GENERATION_TIME in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_GENERATION_TIME])
        cg.add(hub.set_total_generation_time(sens))
    if CONF_SIGNAL_STRENGTH in config:
        sens = await sensor.new_sensor(config[CONF_SIGNAL_STRENGTH])
        cg.add(hub.set_inverter_bluetooth_signal_strength(sens))

    # Textové
    if CONF_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_STATUS])
        cg.add(hub.set_inverter_status_sensor(sens))
    if CONF_SERIAL_NUMBER in config:
        sens = await text_sensor.new_text_sensor(config[CONF_SERIAL_NUMBER])
        cg.add(hub.set_serial_number(sens))
    if CONF_SOFTWARE_VERSION in config:
        sens = await text_sensor.new_text_sensor(config[CONF_SOFTWARE_VERSION])
        cg.add(hub.set_software_version(sens))
    if CONF_DEVICE_TYPE in config:
        sens = await text_sensor.new_text_sensor(config[CONF_DEVICE_TYPE])
        cg.add(hub.set_device_type(sens))
    if CONF_INVERTER_TIME in config:
        sens = await text_sensor.new_text_sensor(config[CONF_INVERTER_TIME])
        cg.add(hub.set_inverter_time_sensor(sens))

    # Binární
    if CONF_GRID_RELAY in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_GRID_RELAY])
        cg.add(hub.set_grid_relay_sensor(sens))
