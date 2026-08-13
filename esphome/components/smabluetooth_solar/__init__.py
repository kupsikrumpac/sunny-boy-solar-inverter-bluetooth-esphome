import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

smabluetooth_solar_ns = cg.esphome_ns.namespace("smabluetooth_solar")
SmaBluetoothSolar = smabluetooth_solar_ns.class_(
    "SmaBluetoothSolar", cg.PollingComponent
)

# Definujeme Enum správně jako C++ scoping class
SmaBluetoothProtocolVersion = smabluetooth_solar_ns.enum(
    "SmaBluetoothProtocolVersion", is_class=True
)

CONF_SMA_INVERTER_BLUETOOTH_MAC = "sma_inverter_bluetooth_mac"
CONF_SMA_INVERTER_PASSWORD = "sma_inverter_password"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(SmaBluetoothSolar),
        cv.Required(CONF_SMA_INVERTER_BLUETOOTH_MAC): cv.string,
        cv.Required(CONF_SMA_INVERTER_PASSWORD): cv.string,
    }
).extend(cv.polling_component_schema("10s"))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    cg.add(var.set_sma_inverter_bluetooth_mac(config[CONF_SMA_INVERTER_BLUETOOTH_MAC]))
    cg.add(var.set_sma_inverter_password(config[CONF_SMA_INVERTER_PASSWORD]))
    
# Vloží přesný C++ typ přímo bez nutnosti překladu přes cg.enum
    cg.add(var.set_protocol_version(cg.RawExpression("esphome::smabluetooth_solar::SmaBluetoothProtocolVersion::SMANET2")))
