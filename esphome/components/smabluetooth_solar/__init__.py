import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, sensor, text_sensor
from esphome.const import (
    CONF_ID,
    CONF_MAC_ADDRESS,
    CONF_PASSWORD,
    CONF_UPDATE_INTERVAL,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_AMPERE,
    UNIT_HERTZ,
    UNIT_KILOWATT_HOURS,
    UNIT_VOLT,
    UNIT_WATT,
)

AUTO_LOAD = ["sensor", "text_sensor", "binary_sensor"]

smabluetooth_solar_ns = cg.esphome_ns.namespace("smabluetooth_solar")
SmaBluetoothSolar = smabluetooth_solar_ns.class_(
    "SmaBluetoothSolar", cg.PollingComponent
)

CONF_TODAY_PRODUCTION = "today_production"
CONF_TOTAL_ENERGY_PRODUCTION = "total_energy_production"
CONF_GRID_FREQUENCY = "grid_frequency"

CONF_POWER_DC_1 = "power_dc_1"
CONF_VOLTAGE_DC_1 = "voltage_dc_1"
CONF_CURRENT_DC_1 = "current_dc_1"

CONF_POWER_DC_2 = "power_dc_2"
CONF_VOLTAGE_DC_2 = "voltage_dc_2"
CONF_CURRENT_DC_2 = "current_dc_2"

CONF_POWER_AC_1 = "power_ac_1"
CONF_VOLTAGE_AC_1 = "voltage_ac_1"
CONF_CURRENT_AC_1 = "current_ac_1"

CONF_STATUS = "status"
CONF_SERIAL_NUMBER = "serial_number"
CONF_SOFTWARE_VERSION = "software_version"
CONF_DEVICE_TYPE = "device_type"
CONF_DEVICE_CLASS = "device_class"
CONF_INVERTER_TIME = "inverter_time"

CONF_GRID_RELAY = "grid_relay"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(SmaBluetoothSolar),
            cv.Required(CONF_MAC_ADDRESS): cv.mac_address,
            cv.Optional(CONF_PASSWORD, default="0000"): cv.string,
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
            cv.Optional(CONF_STATUS): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_SERIAL_NUMBER): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_SOFTWARE_VERSION): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_DEVICE_TYPE): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_DEVICE_CLASS): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_INVERTER_TIME): text_sensor.text_sensor_schema(),
            cv.Optional(CONF_GRID_RELAY): binary_sensor.binary_sensor_schema(),
        }
    )
    .extend(cv.polling_component_schema("10s"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.set_sma_inverter_bluetooth_mac(str(config[CONF_MAC_ADDRESS])))
    cg.add(var.set_sma_inverter_password(config[CONF_PASSWORD]))

    # Sensors
    if CONF_TODAY_PRODUCTION in config:
        sens = await sensor.new_sensor(config[CONF_TODAY_PRODUCTION])
        cg.add(var.set_today_production_sensor(sens))

    if CONF_TOTAL_ENERGY_PRODUCTION in config:
        sens = await sensor.new_sensor(config[CONF_TOTAL_ENERGY_PRODUCTION])
        cg.add(var.set_total_energy_production_sensor(sens))

    if CONF_GRID_FREQUENCY in config:
        sens = await sensor.new_sensor(config[CONF_GRID_FREQUENCY])
        cg.add(var.set_grid_frequency_sensor(sens))

    # PV Input 1
    if CONF_POWER_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_POWER_DC_1])
        cg.add(var.set_active_power_sensor_pv(0, sens))

    if CONF_VOLTAGE_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_VOLTAGE_DC_1])
        cg.add(var.set_voltage_sensor_pv(0, sens))

    if CONF_CURRENT_DC_1 in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_DC_1])
        cg.add(var.set_current_sensor_pv(0, sens))

    # AC Phase 1
    if CONF_POWER_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_POWER_AC_1])
        cg.add(var.set_active_power_sensor(0, sens))

    if CONF_VOLTAGE_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_VOLTAGE_AC_1])
        cg.add(var.set_voltage_sensor(0, sens))

    if CONF_CURRENT_AC_1 in config:
        sens = await sensor.new_sensor(config[CONF_CURRENT_AC_1])
        cg.add(var.set_current_sensor(0, sens))

    # Text Sensors
    if CONF_STATUS in config:
        sens = await text_sensor.new_text_sensor(config[CONF_STATUS])
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

    # Binary Sensors
    if CONF_GRID_RELAY in config:
        sens = await binary_sensor.new_binary_sensor(config[CONF_GRID_RELAY])
        cg.add(var.set_grid_relay_sensor(sens))