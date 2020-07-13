"""Support for awtrix notifications."""
import logging

import voluptuous as vol
import requests

from . import DOMAIN as AWTRIX_DOMAIN

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_MESSAGE,
    ATTR_TARGET,
    ATTR_TITLE,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

from homeassistant.const import (
    CONF_URL,
    HTTP_BAD_REQUEST,
    HTTP_BASIC_AUTHENTICATION,
    HTTP_DIGEST_AUTHENTICATION,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_OK,
)

import homeassistant.helpers.config_validation as cv

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_URL): cv.url,
})

_LOGGER = logging.getLogger(__name__)

def get_service(hass, config, discovery_info=None):
    """Get the Awtrix notification service."""
    _LOGGER.debug("get AWTRIX Service")
    config = hass.data.get(AWTRIX_DOMAIN)
    
    return AwtrixNotificationService(
        config[CONF_URL],
    )

class AwtrixNotificationService(BaseNotificationService):
    """Implement the notification service for awtrix."""

    def __init__(
        self, url,
    ):
        """Initialize the service."""
        self.url = url
        _LOGGER.debug("init Awtrix Service %s",url)

    def _fixcolor(self,col):
        ret = [0, 0, 0]
        if (len(col) ==3):
            ret[0] = min((int(col[0]),255))
            ret[1] = min((int(col[1]),255))
            ret[2] = min((int(col[2]),255))
        return ret

    def _fixarray(self,arr):
        ret = []
        for e in arr[:10]:
            ret.append(int(e))
        return ret

    def _fixint(self,val):
        return max(0,int(val))

    def send_message(self, message="", **kwargs):
        service_data = {"url": self.url}
        
        data = kwargs.get(ATTR_DATA)

        if ATTR_TARGET not in kwargs:
            target = "notify"
        else: 
            target = kwargs.get(ATTR_TARGET)[0]

        if ATTR_TITLE not in kwargs:
            title = "ha-notify"
        else: 
            title = kwargs.get(ATTR_TITLE)

        _LOGGER.debug("Target: %s",target)
        
        if target == "temporaryapp":
            if data.get("name") == None:
                data["name"] = title
            if data.get("lifetime") == None:
                data["lifetime"] = 3
            if data.get("repeat") == None:
                data["repeat"] = 3
            data.pop("force")

        if target == "customapp":
            if data.get("ID") == None:
                data["ID"] = 0
            data.pop("force")

        if target not in ["customapp","notify","temporaryapp"]:
            _LOGGER.warning("Wrong target: %s is invalid.",target)
            return
        
        if message:
            service_data.update({ATTR_MESSAGE: message})
            data["text"] = message
      
        if data.get("icon") != None:
            data["icon"] = self._fixint(data["icon"])

        if data.get("progress") != None:
            data["progress"] = self._fixint(data["progress"])

        if data.get("soundfile") != None:
            data["soundfile"] = self._fixint(data["soundfile"])

        if data.get("color") != None:
            data["color"] =self._fixcolor(data["color"])

        if data.get("progressColor") != None:
            data["progressColor"] =self._fixcolor(data["progressColor"])

        if data.get("progressBackground") != None:
            data["progressBackground"] =self._fixcolor(data["progressBackground"])

        if data.get("barchart") != None:
            data["barchart"] =self._fixarray(data["barchart"])

        if data.get("linechart") != None:
            data["linechart"] =self._fixarray(data["linechart"])

        _LOGGER.warning("Target: %s Data: %s",target,str(data))
        
        headers={"Content-Type: application/json",
                "Accept: application/json"}
        try:
            response = requests.post(self.url+target, json=data)
            _LOGGER.warning("Respone: " + str(response))
        except:
            response = None
            _LOGGER.warning("Error on sending notify")
        
        if (
            response.status_code >= HTTP_INTERNAL_SERVER_ERROR
            and response.status_code < 600
        ):
            _LOGGER.exception(
                "Server error. Response %d: %s:", response.status_code, response.reason
            )
        elif (
            response.status_code >= HTTP_BAD_REQUEST
            and response.status_code < HTTP_INTERNAL_SERVER_ERROR
        ):
            _LOGGER.exception(
                "Client error. Response %d: %s:", response.status_code, response.reason
            )
        elif response.status_code >= HTTP_OK and response.status_code < 300:
            _LOGGER.debug(
                "Success. Response %d: %s:", response.status_code, response.reason
            )
        else:
            _LOGGER.debug("Response %d: %s:", response.status_code, response.reason)
