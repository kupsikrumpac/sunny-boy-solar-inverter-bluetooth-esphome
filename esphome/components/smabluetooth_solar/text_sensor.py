import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor
from . import SmaBluetoothSolar, smabluetooth_solar_ns

DEPENDENCIES = ["smabluetooth_solar"]

CONF_STATUS = "status"
CONF_SERIAL_NUMBER = "serial_number"
CONF_SOFTWARE_VERSION = "software_version"
CONF_DEVICE_TYPE = "device_type"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_SMA_BLUETOOTH_SOLAR_ID): cv.use_id(SmaBluetoothSolar),
        cv.Optional(CONF_STATUS): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_SERIAL_NUMBER): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_SOFTWARE_VERSION): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_DEVICE_TYPE): text_sensor.text_sensor_schema(),
    }
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_SMA_BLUETOOTH_SOLAR_ID])

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
