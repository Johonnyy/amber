import os
import subprocess
import venv
import platform
import argparse

parser = argparse.ArgumentParser(description="Run Amber in different modes.")
parser.add_argument("--debug", action="store_true", help="Run in debug mode")
args = parser.parse_args()

VENVPATH = os.path.abspath("venv")

if not (os.path.exists(VENVPATH) and os.path.isdir(VENVPATH)):
    print("Virtual environment does not exist, creating one now...")
    venv.create(VENVPATH, with_pip=True)
    print("Virtual environment created successfully.")

while True:
    # Find platform
    print("Activating virtual environment...")
    if platform.system() == "Windows":
        print("System detected: Windows")
        activate_script = os.path.join(VENVPATH, "Scripts", "activate")
        pip_script = os.path.join(VENVPATH, "Scripts", "pip")
        python_executable = os.path.join(VENVPATH, "Scripts", "python.exe")
        command = (
            f"{activate_script} && {pip_script} install --quiet -r requirements.txt"
        )
        if not args.debug:
            print("Installing requirements...")
            subprocess.run(command, shell=True)
    else:
        print("System detected: Linux/Mac")
        activate_script = os.path.join(VENVPATH, "bin", "activate")
        pip_script = os.path.join(VENVPATH, "bin", "pip")
        python_executable = os.path.join(VENVPATH, "bin", "python")
        command = f"source {activate_script} && {pip_script} install --quiet -r requirements.txt"
        if not args.debug:
            print("Installing requirements...")
            subprocess.run(command, shell=True, executable="/bin/bash")

    print("Starting Amber...")

    p = subprocess.Popen([python_executable, "main.py"])
    exit_code = p.wait()

    exit_code = abs(exit_code)

    if exit_code == 11:
        print("Restarting now...")
        continue
    else:
        break
