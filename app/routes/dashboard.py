"""from app.dashboard import Dashboard
from flask import Blueprint

dashboard = None


def initDashboardRoute(login_manager, admin):
    dashboardBlueprint = Blueprint("dashboard", __name__, url_prefix="/dashboard")

    global dashboard
    dashboard = Dashboard(login_manager, admin)

    dashboardBlueprint.register_blueprint(dashboard.mainBP)
    dashboardBlueprint.register_blueprint(dashboard.authBP)

    return dashboardBlueprint
"""
