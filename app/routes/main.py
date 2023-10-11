from flask import Blueprint, render_template, request, Response
from app.functions import log
import json

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return "success"


@main_bp.route("/development")
def development():
    return render_template("development.html")


@main_bp.route("/training")
def training():
    return render_template("training.html")


@main_bp.route("/submit-command", methods=["POST"])
def submitCommand():
    data = request.json
    from app.assistant.intention_detection_deprecated_dialogflow import detect_intention

    # detect_intention(data["console"])
    return Response(status=200)


@main_bp.route("/submit-training", methods=["POST"])
def submitTraining():
    data = request.json
    print(data)
    convTurns = []

    for turn in data:
        newTurn = {"role": turn["speaker"], "content": turn["text"]}
        convTurns.append(newTurn)

    trainingData = {"messages": convTurns}

    with open("training.jsonl", "a") as f:
        f.write(json.dumps(trainingData) + "\n")

    return Response(status=200)


@main_bp.route("/dialogflow", methods=["POST"])
def dialogflow():
    log(request)
    return Response(status=200)
    # username: amber
    # TS)Okf+ByN$c^GqTR;wSP2z(ko
    pass
