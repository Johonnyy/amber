from ..devices.local.text_to_speech import generateAudio
from ..functions import *
import random

response_rules = {
    "configureTheme": [
        "Sure {name}, I've set the theme to {value} for you.",
        "Alright {name}, the theme has been updated to {value}.",
        "{name}, your theme is now set to {value}.",
        "Done! The theme is now {value} as you requested {name}.",
        "Theme updated to {value} {name}. Let me know if you need anything else.",
        "You got it {name}! The theme color is now {value}.",
        "Consider it done {name}. I've changed the theme to {value} for you.",
        "Voila {name}, your theme is now in the {value} shade.",
        "Just changed the theme to {value} for you {name}. Hope you like it!",
        "Theme change successful! It's now set to {value} {name}.",
        "I've set the theme to {value} for you {name}.",
    ]
}

error_rules = {
    "errorUnderstanding": [
        "I'm sorry {name}, but I didn't understand that.",
        "Apologies {name}, could you please rephrase your question?",
        "I seem to be having trouble comprehending your input {name}.",
        "I'm having difficulty processing your request at the moment {name}.",
        "Oops {name}, something went wrong on my end. Can you try again?",
        "My apologies {name}, I didn't catch that. Can you repeat?",
        "Sorry {name}, I'm not sure I follow. Could you clarify?",
        "I'm not quite getting that {name}. Can you rephrase?",
        "I'm a bit lost {name}. Mind saying that again?",
        "Sorry for the confusion {name}. Can you provide more details?",
    ]
}

missing_entity = {
    "configureTheme": {
        "value": [
            "What theme would you like {name}?",
            "I noticed you didn't specify a theme {name}. Which one do you have in mind?",
            "Could you let me know which theme you'd prefer {name}?",
            "I'm ready to change the theme for you {name}. Just tell me which one.",
            "Which theme are you thinking of {name}?",
            "I can set the theme for you {name}. Which one would you like?",
            "Please specify the theme you'd like to set {name}.",
            "I'm all ears {name}. Which theme are you referring to?",
            "Help me out a bit {name}. What theme color are you thinking of?",
            "Just let me know the theme you want, and I'll set it for you {name}.",
        ]
    },
    "weather": {
        "location": [
            "Where would you like to check the weather {name}?",
            "I can provide the weather update {name}. Just let me know the location.",
            "Which city or region's weather are you interested in {name}?",
            "Help me out a bit {name}. Where do you want the weather update for?",
            "I'm ready to provide the weather details {name}. Which location are you thinking of?",
            "Please specify the location you'd like the weather for {name}.",
            "I can get that for you {name}. Which place's weather would you like to know?",
            "Sure thing {name}. Just tell me the location, and I'll fetch the weather for you.",
            "Which location's weather are you curious about {name}?",
        ],
        "remember": [
            "Would you like me to remember this location for future weather updates {name}?",
            "Should I save this location for your future requests {name}?",
            "Do you want me to keep this location on file for next time {name}?",
            "Would it be helpful if I remembered this location for you {name}?",
            "How about I save this location for future reference {name}?",
            "Would you prefer if I stored this location for upcoming weather checks {name}?",
            "Should I make a note of this location for the future {name}?",
            "Do you want this location to be your default for weather inquiries {name}?",
            "Would you appreciate it if I kept this location in mind for later {name}?",
        ],
    },
}


@prevent_plugin_access
def generate_response(intent, entities):
    name = generate_name()
    entities["name"] = name
    response_list = response_rules.get(
        intent, f"I'm sorry {name}, there was an error getting the response"
    )
    choice = random.choice(response_list)
    formatted = choice.format(**entities)
    generateAudio(formatted)


@prevent_plugin_access
def generate_premade_response(response):
    name = generate_name()
    formatted = response.format(**name)
    return formatted


@prevent_plugin_access
def generate_error(error, skip=False):
    from app import socket

    if skip:
        socket.emit("alert", error)
        return generateAudio(error)

    name = generate_name()
    response_list = error_rules.get(error, f"I'm sorry {name}, there was an error")
    choice = random.choice(response_list)
    formatted = choice.format(name=name)
    generateAudio(formatted)

    # generateAudio(res, socket)
    # socket.emit("commandResponse", {"response": response.choices[0].message.content})


@prevent_plugin_access
def generate_missing_entity(intent, mi):
    name = generate_name()
    response_list = missing_entity[intent].get(
        mi, f"I'm sorry {name}, there was an error"
    )
    choice = random.choice(response_list)
    formatted = choice.format(name=name)
    generateAudio(formatted)
    from ..devices.local.speech_recognition_manager import listenForValue

    newValue = listenForValue()
    return newValue


def generate_name():
    config = getConfig()

    return random.choice(config["responses"]["names"])
