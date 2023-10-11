from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.functions import log
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

mainBP = Blueprint(
    "main",
    __name__,
    url_prefix="/",
    template_folder=os.path.join(parent_dir, "templates"),
)


@mainBP.route("/")
@login_required
def index():
    return render_template("index.html")


@mainBP.route("/config")
@login_required
def config():
    return render_template("config.html")


@mainBP.route("/usersettings")
@login_required
def usersettings():
    return render_template("usersettings.html")


@mainBP.route("/interactive")
@login_required
def interactive():
    from app.extensions import extensions

    conversation = extensions.openai_manager.conversation

    return render_template("interactive.html", conversation=conversation)


@mainBP.route("/responsemanager")
@login_required
def responsemanager():
    return render_template("responsemanager.html")


@mainBP.route("/conversationlogs")
@login_required
def conversationlogs():
    return render_template("conversationlogs.html")


@mainBP.route("/consolelogs")
@login_required
def consolelogs():
    return render_template("consolelogs.html")


@mainBP.route("/functionmanager")
@login_required
def functionmanager():
    from app.extensions import extensions

    functions = extensions.module_manager.function_instances
    modules = extensions.module_manager.module_instances

    for module in modules:
        module.name = module.__name__.split(".")[-1]
        module.type = module.__name__.split(".")[-2]

    return render_template("functionmanager.html", plugins=functions, modules=modules)


@mainBP.route("/devices")
@login_required
def devices():
    devices = []
    from app.extensions import extensions

    for device in extensions.device_manager.loaded_devices:
        devices.append({"name": device.name, "id": device.id})

    print(devices)

    return render_template("devices.html", devices=devices)


@mainBP.route("/device/<device>")
@login_required
def device(device):
    deviceDict = {}
    from app.extensions import extensions

    deviceInstance = extensions.device_manager.get_device_by_id(device)

    print(deviceDict)

    if not deviceInstance:
        return redirect("/dashboard/devices")

    deviceDict["name"] = deviceInstance.name
    print(deviceDict)

    return render_template("device.html", device=deviceDict)
