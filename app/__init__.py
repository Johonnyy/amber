from flask import Flask, Blueprint
from flask_socketio import SocketIO, Namespace
from app.extensions import extensions
from app.dashboard import Dashboard
from app.local.main import localDevice
from app.functions import getConfig
import logging


class IgnoreSpecificMessageFilter(logging.Filter):
    def filter(self, record):
        # Ignore GET requests to /dashboard/api/getlogs
        return "dashboard/api/getlogs" not in record.getMessage()


# from app.routes import *


class Amber:
    def __init__(self):
        self.extensions = extensions
        self.dashboard = Dashboard()
        self.app = Flask(__name__)

    def startDashboard(self):
        self.app.debug = True
        self.app.secret_key = "W.5$I['UyGE)2u)_Wn]Smfo^OhY41H0t"  # Randomly generated key, doesn't do anything
        self.extensions.socket.init_app(self.app, logger=True)
        self.app.logger.addFilter(IgnoreSpecificMessageFilter())

        self.extensions.login_manager.init_app(self.app)

        dashboardBlueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")

        dashboardBlueprint.register_blueprint(self.dashboard.mainBP)
        dashboardBlueprint.register_blueprint(self.dashboard.authBP)
        dashboardBlueprint.register_blueprint(self.dashboard.apiBP)
        dashboardBlueprint.register_blueprint(self.dashboard.functionBP)

        # setup_socket_routes(socket)
        # app.register_blueprint(routes.socket_bp)

        # app.register_blueprint(routes.main_bp)
        # app.register_blueprint(routes.setup_bp, url_prefix="/setup")
        self.app.register_blueprint(dashboardBlueprint, url_prefix="/dashboard")

        # ssl_context = ("certs/cert.pem", "certs/key.pem")
        self.extensions.socket.run(
            self.app, host="0.0.0.0", port=getConfig()["port"], use_reloader=False
        )

    def startLocalDevice(self):
        localDevice.start()  # Start listening


amber = Amber()
