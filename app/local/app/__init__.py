import eel
import os

from app.functions import getConfig


class AmberLocalApp:
    def __init__(self):
        eel.init(os.path.join("app", "local", "app", "web"))

    def startListening(self):
        eel.showListening()

    def stopListening(self):
        eel.hideListening()

    @eel.expose
    def get_config():
        config = getConfig()
        return config
