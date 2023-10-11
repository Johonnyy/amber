import eel
import os


class AmberLocalApp:
    def __init__(self):
        eel.init(os.path.join("app", "local", "app", "web"))

    def start(self):
        # eel.start("index.html", mode="chrome", cmdline_args=["--kiosk"])
        # eel.start("index.html")
        pass

    def startListening(self):
        eel.showListening()

    def stopListening(self):
        eel.hideListening()
