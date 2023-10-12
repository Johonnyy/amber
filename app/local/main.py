from .porcupine_manager import startListening
from .speech_recognition_manager import startRecording
from .text_to_speech import generateAudio
from app.deviceBase import BaseDevice
from app.deviceAPI import DeviceAPI
from .app import AmberLocalApp
import threading

id = "local-1"


class LocalDevice(BaseDevice):
    def __init__(self):
        super().__init__(
            name="Local 1",
            id=id,
            description="The local device.",
            version="1.0.0",
        )
        self.muted = False
        self.api = DeviceAPI()
        self.guiApp = AmberLocalApp()

    def start(self):
        try:
            # NEEDS TO BE THREADED
            listener = threading.Thread(target=startListening)
            listener.daemon = True
            listener.start()
        except KeyboardInterrupt:
            print("Server stopped by user.")

    def event(self, eventName):
        if eventName == "startListening":
            self.guiApp.startListening()
        elif eventName == "stopListening":
            self.guiApp.stopListening()
        elif eventName == "mute":
            self.muted = True


localDevice = LocalDevice()
