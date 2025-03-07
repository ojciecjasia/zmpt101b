import esphome.codegen as cg
from esphome import pins
import esphome.config_validation as cv

from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    CONF_PIN,
    CONF_FREQUENCY,
    CONF_SENSITIVITY,    
    CONF_SENSOR,
    CONF_NUMBER,
    CONF_ANALOG,
    CONF_INPUT,
    ICON_FLASH,
    UNIT_VOLT,
    STATE_CLASS_MEASUREMENT,
    DEVICE_CLASS_VOLTAGE,
)

from . import (
    zmpt101b_ns,
    validate_adc_pin,
)


ZMPT101BSensor = zmpt101b_ns.class_(
    "ZMPT101BSensor", 
    sensor.Sensor, 
    cg.PollingComponent
)

CONF_ZMPT101B_ID = "ZMPT101B_id"

CONFIG_SCHEMA = (
    sensor.sensor_schema(
        ZMPT101BSensor,
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
        icon=ICON_FLASH,
    )
    .extend(
        {
            cv.GenerateID(CONF_ZMPT101B_ID): cv.use_id(ZMPT101BSensor),
            cv.Required(CONF_PIN): validate_adc_pin,
            cv.Optional(CONF_FREQUENCY, default=50): cv.int_range(min=40, max=70),
            cv.Optional(CONF_SENSITIVITY, default=941.25): cv.float_range(min=0, max=5000),       

        }
    )
    .extend(cv.polling_component_schema("5s"))
)

async def to_code(config):
    var = await sensor.new_sensor(config)
    await cg.register_component(var, config)

    pin = await cg.gpio_pin_expression(config[CONF_PIN])
    cg.add(var.set_pin(pin))
    cg.add(var.set_frequency(config[CONF_FREQUENCY]))
    cg.add(var.set_sensitivity(config[CONF_SENSITIVITY]))

