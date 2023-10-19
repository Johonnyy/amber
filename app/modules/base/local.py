import variables

from app.functions import exit, getConfig, writeConfig


class Mute:
    def __init__(self):
        self.name = "Mute"
        self.description = "Mutes microphone."
        self.version = "1.1.0"
        self.parameters = {
            "type": "object",
            "properties": {},
        }
        self.configOptions = []

    def handle(self, args):
        from app.local.main import localDevice

        localDevice.muted = True

        return "Success"


class ChangeImage:
    def __init__(self):
        self.name = "ChangeImage"
        self.description = "Changes the image source of the local device."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {"source": {"type": "string", "enum": ["nasa", "bing"]}},
        }
        self.configOptions = []

    def handle(self, args):
        source = args["source"]

        config = getConfig()
        config["local"]["source"] = source
        writeConfig(config)

        exit(11)

        return "Success"
