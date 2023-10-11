from app.moduleAPI import log, getCredential, similarFromList

from webcolors import name_to_rgb
import os
import requests
import json

GOVEEURL = "https://developer-api.govee.com/v1/devices/"


def throwError(error):
    log("error at govee throwError: " + error, "error")
    return error


class ControlLightingDevice:
    def __init__(self):
        self.module = "govee"
        self.name = "ControlLightingDevice"
        self.description = "Control lighting devices using the Govee API."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["turnOn", "turnOff", "setColor", "setBrightness"],
                },
                "device": {
                    "type": "string",
                    "description": "The name of the device to control. Use 'el' if you believe it is every light.",
                },
                "color": {
                    "type": "string",
                    "description": "Color to change the device to (optional)",
                },
                "brightness": {
                    "type": "integer",
                    "description": "Brightness to change the device to (optional)",
                },
            },
            "required": ["action", "device"],
        }
        self.configOptions = [
            {
                "value": "apikey",
                "title": "API Key",
                "description": "The API key obtained from the Govee mobile app.",
                "type": "text",
            }
        ]

    def handle(self, args):
        action = args.get("action")
        device = args.get("device")
        color = args.get("color", None)
        percentage = args.get("percentage", None)

        key = getCredential("plugins", self.module, self.name, "apikey")

        if not key:
            return "Error: No API key provided"

        headers = {
            "accept": "application/json",
            "Govee-API-Key": key,
        }

        response = requests.get(f"{GOVEEURL}", headers=headers)

        if (response.status_code) != 200:
            return throwError(f"Error when listing devices: {response.reason}")

        dict = json.loads(response.text)
        dictNames = []
        device_list = dict["data"]["devices"]

        for d in device_list:
            dictNames.append(d["deviceName"])

        dictNames.append("el")
        device_to_find = similarFromList(device, dictNames)

        if device_to_find == "el":
            for d in device_list:
                payload = {
                    "model": d["model"],
                    "device": d["device"],
                    "cmd": {"name": "turn", "value": ""},
                }
                if action == "turnOn":
                    payload["cmd"]["value"] = "on"
                elif action == "turnOff":
                    payload["cmd"]["value"] = "off"
                elif action == "setBrightness":
                    payload["cmd"]["name"] = "brightness"
                    payload["cmd"]["value"] = percentage
                elif action == "setColor":
                    rgb_tuple = name_to_rgb(color)
                    r, g, b = rgb_tuple
                    max_value = max(r, g, b)
                    r_new = r * 255 // max_value
                    g_new = g * 255 // max_value
                    b_new = b * 255 // max_value
                    payload["cmd"]["name"] = "color"
                    payload["cmd"]["value"] = {
                        "name": "Color",
                        "r": r_new,
                        "g": g_new,
                        "b": b_new,
                    }

                response = requests.put(
                    f"{GOVEEURL}control", json=payload, headers=headers
                )

                if (response.status_code) != 200:
                    return throwError(
                        f"Error when controlling device: {response.reason}"
                    )
            return "Success"

        matching_device = next(
            (
                device
                for device in device_list
                if device["deviceName"] == device_to_find
            ),
            None,
        )

        if not matching_device:
            return throwError("There was an error getting the devices")

        headers["content-type"] = "application/json"

        payload = {
            "model": matching_device["model"],
            "device": matching_device["device"],
            "cmd": {"name": "turn", "value": ""},
        }

        if action == "turnOn":
            payload["cmd"]["value"] = "on"
        elif action == "turnOff":
            payload["cmd"]["value"] = "off"
        elif action == "setBrightness":
            payload["cmd"]["name"] = "brightness"
            payload["cmd"]["value"] = percentage
        elif action == "setColor":
            rgb_tuple = name_to_rgb(color)
            r, g, b = rgb_tuple
            max_value = max(r, g, b)
            r_new = r * 255 // max_value
            g_new = g * 255 // max_value
            b_new = b * 255 // max_value
            payload["cmd"]["name"] = "color"
            payload["cmd"]["value"] = {
                "name": "Color",
                "r": r_new,
                "g": g_new,
                "b": b_new,
            }

        response = requests.put(f"{GOVEEURL}control", json=payload, headers=headers)

        if (response.status_code) != 200:
            return throwError(f"Error when controlling device: {response.reason}")

        log("success", "success")
        return "Success"
