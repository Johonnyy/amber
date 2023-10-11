from app.functions import *
from app.assistant.response_manager import *


def handle_config(intent, entities):
    from app import socket

    log(entities)

    configureIntents = {"theme": {"option": "theme", "entity": "theme"}}
    activeIntent = configureIntents[intent]

    # Check if the entity exists

    log(entities[activeIntent["entity"]])

    socket.emit(
        "changeOption",
        {
            "option": activeIntent["option"],
            "value": entities[activeIntent["entity"]]["value"],
        },
    )
