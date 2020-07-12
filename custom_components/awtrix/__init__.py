"""awtrix RGB Matrix Notify"""
import logging

import voluptuous as vol

from homeassistant.const import CONF_URL
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "awtrix"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_URL): cv.url,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
    """Set up the Awtrix."""
    _LOGGER.debug("Setting up awtrix platform")
    conf = config[DOMAIN]
    hass.data[DOMAIN] = {
        "url": conf["url"],
        "drawmode": False,
    }
    
    return True