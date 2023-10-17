from flask import Blueprint, request, jsonify, render_template, Response, redirect
from flask_login import login_required
from app.functions import getLogs, log

# from app.assistant.intention_detection_deprecated_dialogflow import detect_intention
import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

functionBP = Blueprint(
    "function",
    __name__,
    url_prefix="/function",
    template_folder=os.path.join(parent_dir, "templates/function"),
)


@functionBP.route("/editfunction/<type>/<module>/<function>")
@login_required
def plugin(type, module, function):
    from app.extensions import extensions

    pluginData = extensions.module_manager.getFunctionByName(type, module, function)
    inputs = extensions.module_manager.getInput(type, module, function)

    return render_template("function.html", plugin=pluginData, inputs=inputs)


@functionBP.route("/editmodule/<type>/<module>")
@login_required
def pluginEditor(type, module):
    # in module manager add the directory (base/plugin) as a type and then here
    # find the instance by the name and then use that to get just the one file
    languages = [
        {"extension": ".py", "language": "python"},
        {"extension": ".md", "language": "markdown"},
    ]

    from app.extensions import extensions

    instance = extensions.module_manager.getModuleByName(type, module)

    file = instance.__file__
    language = None

    for lang in languages:
        if file.endswith(lang["extension"]):
            language = lang["language"]

    try:
        with open(file, "r") as f:
            content = f.read()
        return render_template(
            "editor.html", file=content, language=language, module=instance
        )
    except Exception as e:
        return render_template("editor.html", file=None, language=None, module=instance)


@functionBP.route("/reloadmodule/<type>/<module>")
@login_required
def reloadModule(type, module):
    from app.extensions import extensions

    extensions.module_manager.reloadModule(type, module)

    return redirect("/dashboard/functionmanager")


@functionBP.route("/<type>/<module>/<function>/submit-setup", methods=["POST"])
@login_required
def pluginSubmitSetup(type, module, function):
    from app.extensions import extensions

    json = request.json
    for input in json:
        extensions.module_manager.setInput(
            type, module, function, input["key"], input["value"]
        )

    extensions.module_manager.load_functions(True)
    extensions.openai_manager.newSession()

    return Response(status=200)


@functionBP.route("/actionmodule/<type>/<module>", methods=["POST"])
@login_required
def pluginEditFile(type, module):
    from app.extensions import extensions

    action = request.json.get("action", None)

    if not action:
        return jsonify({"status": "error", "message": "Unknown action"})

    if action == "rename":
        try:
            prevFile = request.json.get("oldFile", None)
            newFile = request.json.get("newFile", None)
            os.rename(prevFile, newFile)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    elif action == "create":
        try:
            log("create")
            file_path = request.json.get("newFile", None)
            with open(file_path, "w") as f:
                f.write("")  # Create an empty file
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
    elif action == "delete":
        try:
            file_path = request.json.get("oldFile", None)
            os.remove(file_path)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    extensions.module_manager.load_functions(True)
    return jsonify({"status": "success"})


@functionBP.route("/save_file", methods=["POST"])
@login_required
def pluginEditorSaveFile():
    try:
        file_path = request.json.get("file_path")
        file_content = request.json.get("content", "")

        if not file_path:
            return jsonify({"status": "error", "message": "Invalid path"}), 400

        with open(file_path, "w") as f:
            f.write(file_content)

        from app.extensions import extensions

        path = os.path.normpath(file_path)
        path = path.split(os.sep)

        extensions.module_manager.reloadModule(path[-2], path[-1].replace(".py", ""))

        return jsonify({"status": "success", "message": "File saved successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


#
#
#    New Modules/Functions
#
#


@functionBP.route("/createmodule", methods=["GET", "POST"])
@login_required
def createModule():
    if request.method == "POST":
        from app.extensions import extensions

        module_name = request.form["name"]
        module_type = request.form["type"]

        if not module_name.endswith(".py"):
            module_name += ".py"

        path = os.path.join("app", "modules", module_type, module_name)

        module_content = "from app.moduleAPI import *"

        with open(path, "w") as f:
            f.write(module_content)

        extensions.module_manager.load_functions(True)

        return Response(status=200)

    return render_template("newmodule.html")
