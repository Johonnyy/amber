import sys
import os
import threading
import time
import variables
import eel

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import amber
from app.functions import getConfig

# from app.assistant.porcupine_manager import startListening

# if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
#     task_thread = threading.Thread(target=startListening)
#     task_thread.daemon = True
#     task_thread.start()

if __name__ == "__main__":
    try:
        startLocalDevice = threading.Thread(target=amber.startLocalDevice)
        startLocalDevice.daemon = True
        startLocalDevice.start()

        startDashboard = threading.Thread(target=amber.startDashboard)
        startDashboard.daemon = True
        startDashboard.start()

        if getConfig()["local"]["enableGUI"]:
            eel.start("index.html", mode="chrome", block=False)
            # eel.start(
            #     "index.html", mode="chrome", cmdline_args=["--kiosk"], block=False
            # )
            while not variables.stop:
                eel.sleep(1)

            eel.closeApp()

        else:
            while not variables.stop:
                time.sleep(1)

        sys.exit(11)
    except KeyboardInterrupt:
        print("Server stopped by user.")
        variables.stop = True

# ssh -R *:8080:127.0.0.1:8080 johonny@192.168.1.187
