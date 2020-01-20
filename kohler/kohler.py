import json
import requests
from requests.exceptions import ConnectionError

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_TEXT_PLAIN = "text/plain"


class Kohler:
    def __init__(self, kohlerHost):
        self._baseUrl = f"http://{kohlerHost}"

    def btDisconnect(self):
        url = f"{self._baseUrl}/bt_disconnect.cgi"
        return self.fetch(url, None, CONTENT_TYPE_TEXT_PLAIN)

    def languages(self):
        url = f"{self._baseUrl}/languages.cgi"
        return self.fetch(url)

    def lightOff(self, module):
        params = {
            "module": module  # light number
        }

        url = f"{self._baseUrl}/light_off.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def lightOn(self, module=1, intensity=100):
        # min: 0, max: 100, interval: 1
        params = {
            "module": module,  # light number
            "intensity": intensity
        }

        url = f"{self._baseUrl}/light_on.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def lightModule(self, module=2, intensity=100):
        # min: 0, max: 100, interval: 1
        params = {
            "module": module,  # light number
            "intensity": intensity
        }

        url = f"{self._baseUrl}/light_module.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def musicOff(self, volume=100):
        params = {
            "volume": volume
        }
        url = f"{self._baseUrl}/music_off.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def musicOn(self, volume=100):
        # min: 0, max: 100, interval: 1
        params = {
            "volume": volume
        }
        url = f"{self._baseUrl}/music_on.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def rainOff(self, value):
        url = f"{self._baseUrl}/rain_off.cgi"
        return self.fetch(url, None, CONTENT_TYPE_TEXT_PLAIN)

    def rainOn(self, mode, color, effect):
        # min: 0, max: 100, interval: 1
        params = {
            "mode": mode,
            "color": color,
            "effect": effect
        }
        url = f"{self._baseUrl}/rain_on.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def saveVariable(self, index, value):
        params = {
            "index": index,
            "value": value
        }

        url = f"{self._baseUrl}/save_variable.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def setDevice(self, value):
        url = f"{self._baseUrl}/set_device.cgi"
        return self.fetch(url, {"value": value})

    def steamOff(self, value):
        url = f"{self._baseUrl}/steam_off.cgi"
        return self.fetch(url, None, CONTENT_TYPE_TEXT_PLAIN)

    def steamOn(self, temp=110, time=10):
        params = {
            "temp": temp,
            "time": time
        }
        url = f"{self._baseUrl}/steam_on.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def stopUser(self):
        url = f"{self._baseUrl}/stop_user.cgi"
        return self.fetch(url, None, CONTENT_TYPE_TEXT_PLAIN)

    def stopShower(self):
        url = f"{self._baseUrl}/stop_shower.cgi"
        return self.fetch(url, None, CONTENT_TYPE_TEXT_PLAIN)

    def startUser(self, user=1):
        params = {
            "user": user
        }

        url = f"{self._baseUrl}/start_user.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def systemInfo(self):
        url = f"{self._baseUrl}/system_info.cgi"
        return self.fetch(url)

    def values(self):
        url = f"{self._baseUrl}/values.cgi"
        return self.fetch(url)

    def quickShower(self,
                    valve_num=1,
                    valve1_outlet=1,
                    valve1_massage=0,
                    valve1_temp=100,
                    valve2_outlet=0,
                    valve2_massage=0,
                    valve2_temp=100):

        params = {
            "valve_num": valve_num,
            "valve1_outlet": outlet1,
            "valve1_massage": valve1_massage,
            "valve1_temp": valve1_temp,
            "valve2_outlet": outlet2,
            "valve2_massage": valve2_massage,
            "valve2_temp": valve2_temp
        }
        url = f"{self._baseUrl}/quick_shower.cgi"
        return self.fetch(url, params, CONTENT_TYPE_TEXT_PLAIN)

    def fetch(self, url, params=None, contentType=CONTENT_TYPE_JSON):
        try:
            response = requests.get(url, params=params)
        except ConnectionError as ex:
            #HACK: gist.github.com/niemyjski/6ba88dcdca7e76172c58530bac66eada
            responseText = ex.args[0].args[1].line
            if contentType == CONTENT_TYPE_JSON:
                return json.loads(responseText)

            return responseText
        else:
            if contentType == CONTENT_TYPE_JSON:
                return response.json()

            return response.text
