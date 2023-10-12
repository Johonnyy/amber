import importlib
import inspect
import os
import yaml
import subprocess
import sys

from app.functions import log, getConfig, writeConfig
from .pluginBase import BasePlugin

current_dir = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_NAME = "moduleCredentials.yml"


class ModuleManager:
    def __init__(self, plugin_dir="plugins"):
        dir = os.path.join(current_dir, plugin_dir)

        self.plugin_dir = plugin_dir
        self.dir = dir
        self.function_instances = []
        self.module_instances = []
        self.libaries = []

    def load_functions(self):
        log("loading modules")
        config = getConfig()

        self.function_instances = []
        self.module_instances = []

        #         plugin_module = importlib.import_module(plugin_path)
        # classes = inspect.getmembers(plugin_module, inspect.isclass)

        for folder in config["modules"]["paths"]:
            path = f"app/modules/{folder}"
            plugin_files = [f[:-3] for f in os.listdir(path) if f.endswith(".py")]
            for plugin_file in plugin_files:
                retries = 3  # Number of retries
                while retries > 0:
                    try:
                        # Step 2: Dynamic Import
                        modulePath = path.replace("/", ".")
                        plugin_module = importlib.import_module(
                            f"{modulePath}.{plugin_file}"
                        )

                        self.module_instances.append(plugin_module)

                        # Step 3: Class Inspection
                        classes = inspect.getmembers(plugin_module, inspect.isclass)

                        # Step 4 and 5: Function Check and Registration
                        for name, obj in classes:
                            name = plugin_file + name
                            try:
                                if hasattr(obj, "handle"):
                                    instance = obj()
                                    instance.type = folder
                                    instance.module = plugin_file
                                    self.function_instances.append(instance)
                                    log(
                                        f"Loaded function: {instance.type}/{instance.module}/{instance.name}",
                                        "success",
                                    )
                            except Exception as e:
                                log("Error at loading module: " + name, "error")
                                log(e, "danger")

                        break
                    except ModuleNotFoundError as e:
                        missing_module_name = str(e).split("'")[
                            1
                        ]  # Extract the missing module name from the error message
                        log(
                            f"Missing dependency: {missing_module_name}. Attempting to install...",
                            "warning",
                        )
                        subprocess.check_call(
                            [
                                sys.executable,
                                "-m",
                                "pip",
                                "install",
                                missing_module_name,
                            ]
                        )
                        log(
                            f"Installed missing dependency: {missing_module_name}",
                            "success",
                        )
                        retries -= 1  # Decrement the retry counter
                    except Exception as e:
                        log("Error at loading module: " + plugin_file, "error")
                        log(e, "danger")
                        break  # Exit the loop if an unknown error occurs

        log("loaded all modules", "success")

    def getFunctionByName(self, type, moduleName, name):
        for module in self.function_instances:
            if (
                (module.name == name)
                & (module.module == moduleName)
                & (module.type == type)
            ):
                return module
        return None

    def getModuleByName(self, type, moduleName):
        for module in self.module_instances:
            # log(module.__name__) app.modules.base.weather
            # log(module.__file__) C:\Users\johnn\Documents\Projects\amber\app\modules\base\weather.py
            modulePath = module.__file__.split("\\")[-1].replace(".py", "")
            typePath = module.__file__.split("\\")[-2]

            if (modulePath == moduleName) & (typePath == type):
                return module

        return None

    def setInput(self, type, module, name, inputKey, inputValue):
        with open(os.path.join(current_dir, CREDENTIALS_NAME), "a+") as f:
            f.seek(0)  # Move file pointer to the beginning of the file
            pluginCredentials = yaml.safe_load(f)  # Load the YAML data

        if pluginCredentials is None:
            pluginCredentials = {}

        if type not in pluginCredentials:
            pluginCredentials[type] = {}

        if module not in pluginCredentials[type]:
            pluginCredentials[type][module] = {}

        if name not in pluginCredentials[type][module]:
            pluginCredentials[type][module][name] = {}

        pluginCredentials[type][module][name][inputKey] = inputValue

        with open(os.path.join(current_dir, CREDENTIALS_NAME), "w") as file:
            yaml.safe_dump(pluginCredentials, file)

    def getInput(self, type, module, name, inputKey=None):
        with open(os.path.join(current_dir, CREDENTIALS_NAME), "a+") as f:
            f.seek(0)  # Move file pointer to the beginning of the file
            pluginCredentials = yaml.safe_load(f)  # Load the YAML data

        if pluginCredentials == None:
            return None

        typeDict = pluginCredentials.get(type, None)

        if not typeDict:
            return None

        moduleDict = typeDict.get(module, None)

        if not moduleDict:
            return None

        nameDict = moduleDict.get(name, None)

        if not nameDict:
            return None

        if not (inputKey):
            return nameDict

        return nameDict.get(inputKey, None)
