from .io_blueprint import IOBlueprint
from flask_socketio import send, emit
import os
import sys
import subprocess
from ..functions import *

"""
socket_bp = IOBlueprint("socket_bp", __name__)


@socket_bp.on("connect")
def handle_connect():
    print("connected")
    config = getConfig()
    if not config["setup"]:
        print("not setup, running setup")
        emit("runSetup")


@socket_bp.on("client_message")
def handle_client_message(data):
    print("Received:", data)
    send("Server received your message: " + data)


@socket_bp.on("restart")
def handle_restart(data):
    restart_backend()


def restart_backend():
    print("Restarting backend...")

    # Get the command used to run the script
    command = [sys.executable] + sys.argv

    # Start a new process with the same command
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Exit the current process
    sys.exit()
"""
