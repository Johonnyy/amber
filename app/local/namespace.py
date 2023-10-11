from flask_socketio import Namespace, emit
from app.functions import log


class DeviceNamespace(Namespace):
    def __init__(self, namespace):
        super().__init__(namespace)

    def on_connect(self):
        log("Device local-1 connected")
        emit("status", {"data": "Connected"})

    def on_disconnect(self):
        print("Client disconnected")
