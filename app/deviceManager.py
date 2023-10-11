import importlib
import os
from app.deviceBase import BaseDevice
from app.functions import log


class DeviceManager:
    def __init__(self, device_dir="devices"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dir = os.path.join(current_dir, device_dir)

        self.device_dir = device_dir
        self.device_ids = [
            d
            for d in os.listdir("app/devices")
            if os.path.isdir(os.path.join("app", "devices", d))
        ]
        self.dir = dir
        self.loaded_devices = []
        self.disabled_devices = []

    def load_devices(self, socket):
        log("loading devices")
        for device_name in os.listdir(self.dir):
            if os.path.isdir(os.path.join("app", self.device_dir, device_name)):
                device_module_path = f"app.{self.device_dir}.{device_name}.main"
                device_module = importlib.import_module(device_module_path)
                if hasattr(device_module, "Device") and issubclass(
                    device_module.Device, BaseDevice
                ):
                    instance = device_module.Device()
                    res = instance.start()
                    log("Loaded device: " + instance.name)
                    self.loaded_devices.append(instance)

                # Namespace

                module = importlib.import_module(
                    f"app.{self.device_dir}.{device_name}.namespace"
                )
                namespace_class = getattr(module, "DeviceNamespace")
                socket.on_namespace(namespace_class(f"/device/{device_name}"))
                log("Loaded device namespace: " + instance.name)

    def get_device_by_id(self, id):
        for device in self.loaded_devices:
            if device.id == id:
                return device
        return None
