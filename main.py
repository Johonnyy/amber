import sys
import os
import threading

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import amber
from app.functions import log

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

        amber.startDashboard()
    except KeyboardInterrupt:
        print("Server stopped by user.")


# ssh -R *:8080:127.0.0.1:8080 johonny@192.168.1.187
