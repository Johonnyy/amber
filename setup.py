from cx_Freeze import setup, Executable

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

# Dependencies are automatically detected, but it might need fine-tuning.
build_exe_options = {
    "packages": ["pvporcupine","engineio","socketio","flask_socketio","threading","time","queue"],  # Add any required packages here
    "excludes": [],     # List of modules to exclude from the final executable
    "include_files": ["custom_wake_words/", "config.yml"]  # Include additional files and directories
}

setup(
    name="AmberBackend",
    version="0.1",
    description="The backend for the voice assistant Amber made by Johonny",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py")]
)
