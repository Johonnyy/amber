from flask import Blueprint, request, redirect, Response, jsonify
from flask_login import login_required
from app.functions import getLogs, log, getConfig, writeConfig, exit

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

apiBP = Blueprint(
    "api",
    __name__,
    url_prefix="/api",
    template_folder=os.path.join(parent_dir, "templates"),
)


@apiBP.route("/")
@login_required
def index():
    return redirect("/dashboard")

@apiBP.route("/restart")
@login_required
def restart():
    exit(11)


@apiBP.route("/getlogs")
@login_required
def getlogs():
    return Response(getLogs(), content_type="text/plain; charset=utf-8")


@apiBP.route("/getconfig")
@login_required
def getconfig():
    return jsonify(getConfig())


@apiBP.route("/writeconfig", methods=["POST"])
@login_required
def writeconfig():
    data = request.json
    writeConfig(data)
    return Response(status=200)


@apiBP.route("/reloadplugins")
@login_required
def reloadPlugins():
    from app.extensions import extensions

    extensions.module_manager.load_functions()
    return Response(status=200)


@apiBP.route("/submit-command", methods=["POST"])
@login_required
def submitCommand():
    from app.extensions import extensions

    data = request.json

    if data.get("newConvo", False):
        extensions.openai_manager.newSession()
        return Response(status=200)

    if data.get("console", "") == "":
        return

    extensions.openai_manager.newUserMessage(data["console"])
    return extensions.openai_manager.messages
