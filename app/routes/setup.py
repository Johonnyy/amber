from flask import Blueprint, render_template, jsonify, request
import json
from app.functions import *

isBeingSetup = False
data = []

dirname = os.path.dirname(__file__)

setup_bp = Blueprint(
    "setup", __name__, template_folder=os.path.join(dirname, "templates")
)


def startSetup(newData):
    global data
    global isBeingSetup
    data = json.dumps(newData)
    isBeingSetup = True


@setup_bp.route("/")
def index():
    if not isBeingSetup:
        return "404"
    return render_template("setup.html")


@setup_bp.route("/get-inputs")
def get_inputs():
    return data


@setup_bp.route("/submit-inputs", methods=["POST"])
def submit_inputs():
    newData = request.json

    from app.moduleAPI import currentInitializingPlugin, resetInitializingPlugin

    pluginName = currentInitializingPlugin
    resetInitializingPlugin()

    from app.intention_detection import plugin_manager

    plugin_manager.sendInitData(pluginName, newData)

    global data
    data = []
    global isBeingSetup
    isBeingSetup = False

    # Here you can process or store the data as needed
    log(newData)
    return jsonify({"message": "Data received successfully!"})
