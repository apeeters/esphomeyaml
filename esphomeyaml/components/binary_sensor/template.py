import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml.components import binary_sensor
from esphomeyaml.const import CONF_LAMBDA, CONF_MAKE_ID, CONF_NAME
from esphomeyaml.helpers import App, Application, process_lambda, variable, optional, bool_

MakeTemplateBinarySensor = Application.MakeTemplateBinarySensor

PLATFORM_SCHEMA = cv.nameable(binary_sensor.BINARY_SENSOR_PLATFORM_SCHEMA.extend({
    cv.GenerateID(CONF_MAKE_ID): cv.declare_variable_id(MakeTemplateBinarySensor),
    vol.Required(CONF_LAMBDA): cv.lambda_,
}))


def to_code(config):
    template_ = None
    for template_ in process_lambda(config[CONF_LAMBDA], [],
                                    return_type=optional.template(bool_)):
        yield
    rhs = App.make_template_binary_sensor(config[CONF_NAME], template_)
    make = variable(config[CONF_MAKE_ID], rhs)
    binary_sensor.setup_binary_sensor(make.Ptemplate_, make.Pmqtt, config)


BUILD_FLAGS = '-DUSE_TEMPLATE_BINARY_SENSOR'
