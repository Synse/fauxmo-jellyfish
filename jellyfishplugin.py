"""Fauxmo plugin for controlling JellyFish lighting.

The on and off methods send the `toCtlrSet` command to the JellyFish controller
websocket with a state of `1` or `0` respectively. This logic is based on the
jellyroll library here: https://github.com/dotchance/jellyroll and documentation
here: https://github.com/parkerjfl/JellyfishLightingAPIExplorer

Faxumo will fake the current state as the last action sent to the controller.

Example config:

```
{
    "FAUXMO": {
        "ip_address": "auto"
    },
    "PLUGINS": {
        "JellyFishPlugin": {
            "path": "~/fauxmo-jellyfish/jellyfishplugin.py",
            "DEVICES": [
                {
                    "port": 12300,
                    "name": "JellyFish Lights",
                    "controller_ip": "192.168.3.1",
                    "zones": ["All Lights"]
                },
                {
                    "port": 12301,
                    "name": "Garage Lights",
                    "controller_ip": "192.168.3.1",
                    "pattern": "Holidays/Valentines Day",
                    "zones": ["Front", "Back"]
                }
            ]
        }
    }
}
```

Dependencies:
    websocket-client
"""
from fauxmo.plugins import FauxmoPlugin
from json import loads
from typing import Sequence
from websocket import create_connection


class JellyFishPlugin(FauxmoPlugin):
    """Fauxmo plugin to interact with a JellyFish lighting controller."""

    def __init__(
        self,
        *,
        port: int,
        name: str,
        controller_ip: str = "192.168.3.1",
        pattern: str = "",
        zones: Sequence[str] = "",
    ) -> None:
        """Initialize an JellyFishPlugin instance.

        Kwargs:
            name: device name
            port: Port for Fauxmo to make this device available to Amazon Echo

            controller_ip: IP address of the JellyFish controller
            pattern: The pattern file to use (optional, default is the current pattern)
            zones: The zone name(s) to turn on/off (optional, default is all zones)
        """
        print('JellyFishPlugin intialized for device "%s"' % name)
        self.controller_ip = controller_ip
        self.pattern = pattern
        self.zones = '","'.join(zones)

        super().__init__(name=name, port=port)

    def on(self) -> bool:
        """Turn on JellyFish lighting zone(s).

        Returns:
            True if device seems to have been turned on, False otherwise.
        """
        self.configure_zones()
        self.validate_pattern()
        print('Turning on "%s" with pattern "%s" for zones ["%s"]' % (self.name, self.pattern, self.zones))
        cmd = '{"cmd":"toCtlrSet","runPattern":{"file":"%s","data":"","id":"","state":1,"zoneName":["%s"]}}' % (self.pattern, self.zones)

        try:
            print('  send >> %s' % cmd)
            ws = create_connection('ws://%s:9000/ws/' % self.controller_ip)
            ws.send(cmd)
            print('  recv << %s' % ws.recv())
            ws.close()

            return True
        except Exception as e:
            print('JellyFish controller error: %s' % e)

        return False

    def off(self) -> bool:
        """Turn off JellyFish lighting zone(s).

        Returns:
            True if device seems to have been turned off, False otherwise.
        """
        self.configure_zones()
        self.validate_pattern()
        print('Turning off "%s" with pattern "%s" for zones ["%s"]' % (self.name, self.pattern, self.zones))
        cmd = '{"cmd":"toCtlrSet","runPattern":{"file":"%s","data":"","id":"","state":0,"zoneName":["%s"]}}' % (self.pattern, self.zones)

        try:
            print('  send >> %s' % cmd)
            ws = create_connection('ws://%s:9000/ws/' % self.controller_ip)
            ws.send(cmd)
            print('  recv << %s' % ws.recv())
            ws.close()

            return True
        except Exception as e:
            print('JellyFish controller error: %s' % e)

        return False

    def get_state(self) -> str:
        """State is faked by fauxmo as the last state sent to the controller."""
        return super().get_state()

    def configure_zones(self) -> None:
        """If zones are unconfigured, get all zones from the controller and update the configuration."""
        cmd = '{"cmd":"toCtlrGet","get":[["zones"]]}'

        # only get zones if unconfigured
        if self.zones != '':
            return

        # get zones from the controller
        try:
            # print('  send >> %s' % cmd)
            ws = create_connection('ws://%s:9000/ws/' % self.controller_ip)
            ws.send(cmd)
            ws_resp = ws.recv()
            # print('  recv << %s' % ws_resp)
            ws.close()
        except Exception as e:
            print('JellyFish controller error: %s' % e)

        # parse zone names
        try:
            json = loads(ws_resp).get('zones')
            zones = [z for z in json.keys()]
        except Exception as e:
            print('Error parsing JSON from JellyFish controller: %s' % e)

        print('Setting zones to "%s"' % '","'.join(zones))
        self.zones = '","'.join(zones)

    def validate_pattern(self) -> None:
        """Confirms that the configured pattern is known to the controller.

        If the pattern is not known, override it with "" to avoid locking up the controller.
        https://github.com/parkerjfl/JellyfishLightingAPIExplorer/issues/2
        """
        cmd = '{"cmd":"toCtlrGet","get":[["patternFileList"]]}'

        # empty pattern is always valid
        if self.pattern == '':
            return

        # get patterns from the controller
        try:
            # print('  send >> %s' % cmd)
            ws = create_connection('ws://%s:9000/ws/' % self.controller_ip)
            ws.send(cmd)
            ws_resp = ws.recv()
            # print('  recv << %s' % ws_resp)
            ws.close()
        except Exception as e:
            print('JellyFish controller error: %s' % e)

        # convert response to a list and look for the configured pattern
        try:
            json = loads(ws_resp).get('patternFileList')
            valid_patterns = [p.get('folders') + '/' + p.get('name') for p in json if p.get('name')]

            if self.pattern in valid_patterns:
                return
        except Exception as e:
            print('Error parsing JSON from JellyFish controller: %s' % e)

        print('Pattern "%s" is invalid, overriding with ""' % self.pattern)
        self.pattern = ''
