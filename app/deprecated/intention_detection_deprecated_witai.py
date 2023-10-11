from wit import Wit

# from .response_manager import generate_response
from ..assistant.response_manager import *
from ..moduleManager import PluginManager
from ..managers import *
from ..functions import *
from ..handlers import *
import importlib
import pkgutil
import os
import random

plugin_manager = PluginManager()
plugin_manager.load_plugins()


@prevent_plugin_access
def reload_plugins():
    plugin_manager.load_plugins()


@prevent_plugin_access
def witmessage(message):
    client = Wit(getConfig()["responses"]["witKey"])
    resp = client.message(message)
    return resp


@prevent_plugin_access
def detect_intention(message, askForRemember=False):
    from app import socket

    resp = witmessage(message)
    log(resp)

    if not resp["intents"]:
        log("error: no intent")
        log(resp)
        return generate_error(
            "errorUnderstanding",
            socket,
        )

    log("got intention")

    intent = resp["intents"][0]["name"]
    entities = resp["entities"]

    log(intent)
    if intent == "wit$cancel":
        return

    if intent.startswith("configure"):
        response = handle_config(message, intent, entities)
        if response["response"] == "missing_entity":
            message = response["message"]
            return detect_intention(message)
        elif response["response"] == "success":
            return
    elif intent.startswith("weather"):
        response = handle_weather(message, intent, entities, askForRemember)
        if response["response"] == "missing_entity":
            message = response["message"]
            return detect_intention(message, True)
    elif intent.startswith("plugin"):
        response = handle_plugin(message, intent, entities)
        return
    # Checked all built in intents

    plugin = plugin_manager.get_plugin_for_intent(intent)
    plugin.handle(intent, entities)

    from ..devices.local.porcupine_manager import set_state

    set_state("LISTENING")


def detectYesorNo(message):
    response = witmessage(message)
    intent = response["intents"][0]["name"]
    log(intent)
    return intent == "wit$confirmation"
