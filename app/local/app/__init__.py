import eel
import os

from app.functions import getConfig


class AmberLocalApp:
    def __init__(self):
        eel.init(os.path.join("app", "local", "app", "web"))

    def start(self):
        if getConfig()["enableGUI"]:
            eel.start("index.html", mode="chrome", cmdline_args=["--kiosk"])

    def startListening(self):
        eel.showListening()

    def stopListening(self):
        eel.hideListening()
