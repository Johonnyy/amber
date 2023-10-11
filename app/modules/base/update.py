from app.moduleAPI import log, getCredential

import requests
import sys
import os
import subprocess

REPOSITORYURL = "https://github.com/Johonnyy/amber.git"
VERSIONURL = "https://raw.githubusercontent.com/Johonnyy/amber/main/version.txt"
VERSIONPATH = "version.txt"


class Update:
    def __init__(self):
        self.name = "Update"
        self.description = "Get latest release from Github and update."
        self.version = "1.0.0"
        self.parameters = {
            "type": "object",
            "properties": {},
        }
        self.configOptions = []
        self.requirements = []

    def handle(self, args):
        githubVersion = None
        localVersion = None

        try:
            response = requests.get(VERSIONURL)
            response.raise_for_status()  # Raise HTTPError for bad responses
            githubVersion = (
                response.text.strip()
            )  # Remove any leading/trailing white spaces
        except requests.RequestException as e:
            log(f"An error occurred while fetching the version: {e}", "error")
            return f"Error fetching version: {e}"

        try:
            with open(VERSIONPATH, "r") as f:
                localVersion = (
                    f.read().strip()
                )  # Remove any leading/trailing white spaces
        except FileNotFoundError:
            print("Local version file not found.")
            return "Local version file not found."
        except IOError as e:
            print(f"An error occurred while reading the local version: {e}")
            return f"Error reading local version: {e}"

        if not (githubVersion or localVersion):
            return "Could not find one of the versions"

        result = self.compare_versions(localVersion, githubVersion)

        if result == False:
            return "up to date"

        try:
            # Execute git pull
            result = subprocess.run(
                ["git", "pull"], capture_output=True, text=True, check=True
            )

            # Check the result
            if result.returncode == 0:
                log("Successfully updated from the repository.", "success", "BOLD")
            else:
                log("Successfully updated from the repository.", "error", "BOLD")
                print(result.stderr)

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while updating the repository: {e}")

        sys.exit(0)

    def compare_versions(self, local_version, github_version):
        local_version.replace(" ", "").replace(".", "").replace("v", "").replace(
            "version", ""
        )
        github_version.replace(" ", "").replace(".", "").replace("v", "").replace(
            "version", ""
        )

        if int(local_version) == int(github_version):
            return False
        elif int(local_version) < int(github_version):
            return True
