# fauxmo-jellyfish
A [fauxmo](https://github.com/n8henrie/fauxmo) plugin to control [JellyFish Lighting](https://www.jellyfishlighting.com/).

Enables Amazon Echo (Alexa) control (**on** and **off** for one or more zones) of JellyFish Lighting via an emulated Belkin WeMo switch and the JellyFish controller websocket.

## Usage

Tested on a Raspberry Pi 4 Model B. Setting a static IP for your JellyFish controller and Raspberry Pi is strongly recommended.

1. Install Python: `sudo apt-get update && sudo apt-get install python3 python3-pip`
2. Install Python dependencies: `pip3 install fauxmo websocket-client`
3. Clone this repo: `git clone https://github.com/Synse/fauxmo-jellyfish.git && cd fauxmo-jellyfish`
4. Update `config.json` with the plugin `path`, your JellyFish `controller_ip`, and JellyFish `zone_names`
5. Start fauxmo: `fauxmo -c config.json`
6. Say **Alexa discover devices** and wait for discovery to finish

Turn lights on/off with **"Alexa turn on JellyFish Lights"** and **"Alexa turn off JellyFish Lights"**.

**Note:** Device discovery may fail if "light" or "switch" doesn't appear in the device name; you can rename the device in the Alexa app after it's discovered.

## References
- https://github.com/dotchance/jellyroll
- https://github.com/parkerjfl/JellyfishLightingAPIExplorer
- https://github.com/vinenoobjelly/jellyfishlights-py
