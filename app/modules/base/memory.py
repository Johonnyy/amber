import os
import json

from app.functions import log

MEM_PATH = os.path.join("databases", "memory.json")


class Remember:
    def __init__(self):
        self.name = "Remember"
        self.description = "Remember information the user tells you."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "Item to remember including context. Required be in format: 'User's name is John Doe.', etc.",
                }
            },
            "required": ["item"],
        }
        self.configOptions = []

    def handle(self, args):
        item = args["item"]

        log("item: " + item, "error")

        with open(MEM_PATH) as f:
            data = json.load(f)

        log("data: " + str(data), "error")

        index = len(data)

        log("index: " + str(index), "error")

        data.append({"index": index, "item": item})

        log("data: " + str(data), "error")

        with open(MEM_PATH, "w") as f:
            json.dump(data, f, indent=4)

        return "Success"


class Forget:
    def __init__(self):
        self.name = "Forget"
        self.description = "Forget information the user tells you."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {
                "index": {"type": "integer", "description": "Index of item to forget"}
            },
            "required": ["index"],
        }
        self.configOptions = []

    def handle(self, args):
        index = args["index"]

        with open(MEM_PATH) as f:
            data = json.load(f)

        del data[index]

        with open(MEM_PATH, "w") as f:
            json.dump(data, f, indent=4)

        return "Success"


class Reset:
    def __init__(self):
        self.name = "Reset"
        self.description = "Resets your memory and forgets everything."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {},
        }
        self.configOptions = []

    def handle(self, args):
        with open(MEM_PATH) as f:
            data = json.load(f)

        data = []

        with open(MEM_PATH, "w") as f:
            json.dump(data, f, indent=4)

        return "Success"
