from flask import Blueprint, render_template, redirect, request, Response
from flask_login import UserMixin, login_user, logout_user, login_required

from app.extensions import extensions
from app.functions import getConfig, writeConfig

import os


class User(UserMixin):
    def __init__(self, id):
        self.id = id


authBP = Blueprint("authBP", __name__, url_prefix="/auth")

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


@extensions.login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return User(user_id)
    return None


@authBP.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == getConfig()["adminPass"]:
            login_user(User(username))
            return redirect("/dashboard")
    return render_template("login.html")


@authBP.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/dashboard/auth/login")


@authBP.route("/changepass", methods=["POST"])
@login_required
def changepass():
    newPass = request.form["password"]

    config = getConfig()
    config["adminPass"] = newPass
    writeConfig(config)

    return redirect("/dashboard/usersettings")
