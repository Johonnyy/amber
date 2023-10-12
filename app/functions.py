import datetime
import yaml
import os
import sys
import inspect
import functools
import logging
import time
import shutil
import eel

from difflib import SequenceMatcher


class IgnoreSpecificMessageFilter(logging.Filter):
    def filter(self, record):
        # Ignore GET requests to /dashboard/api/getlogs
        return "GET /dashboard/api/getlogs" not in record.getMessage()


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

log_file_path = "console.log"


for _ in range(3):
    try:
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
    except PermissionError:
        time.sleep(1)

ignore_filter = IgnoreSpecificMessageFilter()
logging.basicConfig(filename=log_file_path, level=logging.INFO)
logging.getLogger("werkzeug").addFilter(ignore_filter)


def prevent_plugin_access(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the current frame
        current_frame = inspect.currentframe()

        # Get the outer frame (caller)
        caller_frame = inspect.getouterframes(current_frame, 2)

        # Get the module name of the caller
        caller_module = inspect.getmodule(caller_frame[1][0])

        # If the caller module is part of a plugin, return early
        if "plugins" in caller_module.__name__:
            print(f"Function {func.__name__} called from a plugin. Exiting early.")
            return

        # Otherwise, execute the original function
        return func(*args, **kwargs)

    return wrapper


def frozen():
    if getattr(sys, "frozen", False):
        return True
    else:
        return False


def get_base_dir():
    if frozen():
        # The application is bundled
        return os.path.dirname(sys.executable)
    else:
        # The application is run from a script
        return os.path.dirname(os.path.abspath(__file__))

def exit(code):
    eel.close_page()
    sys.exit(code)

def log(data: str = "", severity: str = "info", color: str = None):
    """Logs data to the console and to the web dashboard \n
    Severities:\n
     - info (light blue)
     - success (green)
     - warning (yellow)
     - error (red)\n

    Colors:\n
     - HEADER (purple)
     - OKBLUE (blue)
     - OKCYAN (cyan)
     - OKGREEN (green)
     - WARNING (yellow)
     - FAIL (red)
     - ENDC (white)
     - BOLD (bold)
     - UNDERLINE (underlined)
    """

    stack = inspect.stack()
    caller_frame = stack[1]
    filename = caller_frame.filename
    line_number = caller_frame.lineno

    severities = {
        "info": {"color": bcolors.OKCYAN, "function": logging.info},
        "success": {"color": bcolors.OKGREEN, "function": logging.info},
        "warning": {"color": bcolors.WARNING, "function": logging.warning},
        "error": {"color": bcolors.FAIL, "function": logging.error},
    }

    try:
        useSeverity = severities[severity]
    except KeyError as e:
        return log("No such thing as severity " + severity, "error", "BOLD")

    useColor = ""

    if color:
        try:
            useColor = getattr(bcolors, color)
        except KeyError as e:
            return log("No such thing as color " + color, "error", "BOLD")

    timestamp = (
        # f"{filename.split('amber')[1]}: {line_number}\n"
        "Timestamp: {:%Y-%m-%d %H:%M:%S} - ".format(datetime.datetime.now())
        + useSeverity["color"]
        + useColor
    )
    message = timestamp + str(data) + bcolors.ENDC
    useSeverity["function"](message)
    print(message)


def getLogs():
    with open("console.log", "r") as f:
        logs = f.read()
    return logs


@prevent_plugin_access
def getConfig():
    base_path = get_base_dir()

    if not os.path.exists("config.yml") and os.path.exists("config.yml.example"):
        shutil.copyfile("config.yml.example", "config.yml")

    try:
        if frozen():
            return yaml.safe_load(open(os.path.join(base_path, "config.yml")))
        else:
            return yaml.safe_load(
                open(os.path.join(os.path.dirname(base_path), "config.yml"))
            )
    except FileNotFoundError as e:
        log(
            "Could not find config file! Copy it from the config.yml.example",
            "error",
            "BOLD",
        )


@prevent_plugin_access
def writeConfig(data):
    base_path = get_base_dir()

    if frozen():
        with open(os.path.join(base_path, "config.yml"), "w") as file:
            yaml.safe_dump(data, file)
    else:
        with open(os.path.join(os.path.dirname(base_path), "config.yml"), "w") as file:
            yaml.safe_dump(data, file)


def similar(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio()


def similarFromList(string: str, list: list):
    min_distance = 0
    most_similar = None

    for s in list:
        distance = similar(string, s)
        log(distance)
        if distance > min_distance:
            min_distance = distance
            most_similar = s
    return most_similar
