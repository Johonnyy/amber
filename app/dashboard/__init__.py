from app.dashboard.routes import *
from app.functions import *


class Dashboard:
    def __init__(self):
        self.mainBP = mainBP
        self.authBP = authBP
        self.apiBP = apiBP
        self.functionBP = functionBP
