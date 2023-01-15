# fauxmo-jellyfish
A [fauxmo](https://github.com/n8henrie/fauxmo) plugin to control [JellyFish Lighting](https://www.jellyfishlighting.com/).

Enables Amazon Echo (Alexa) control (on/off state and pattern for one or more zones) of JellyFish Lighting via an emulated Belkin WeMo switch and the JellyFish controller websocket.

## Usage

Tested on a Raspberry Pi 4 Model B, Python 3.9.2, JellyFish controller version 030015, and fauxmo v0.6.0. Setting a static IP for your JellyFish controller and Raspberry Pi is strongly recommended.

1. Install Python: `sudo apt-get update && sudo apt-get -y install python3 python3-pip`
2. Clone this repo: `git clone https://github.com/Synse/fauxmo-jellyfish.git && cd fauxmo-jellyfish`
3. Install Python dependencies: `pip3 install -f requirements.txt`
4. Update `config.json` with the plugin `path`, your JellyFish `controller_ip`, `pattern` (optional, default is current/last pattern), and `zones` (optional, default is all zones)
5. Start fauxmo: `fauxmo -c config.json`
6. Say **Alexa discover devices** and wait for discovery to finish

Turn lights on/off with **"Alexa turn on JellyFish Lights"** and **"Alexa turn off JellyFish Lights"**.

**Note:** Device discovery may fail if "light" or "switch" doesn't appear in the device name; you can rename the device in the Alexa app after it's discovered.

## References
- https://github.com/dotchance/jellyroll
- https://github.com/parkerjfl/JellyfishLightingAPIExplorer
- https://github.com/vinenoobjelly/jellyfishlights-py
- https://github.com/bdunn44/hass-jellyfish-lighting
