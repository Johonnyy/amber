from app.functions import log, similarFromList
import requests
import subprocess
import os
import shutil

PLUGIN_PATH = os.path.join("app", "plugins")
GITHUB_URL = "https://api.github.com/orgs/Amber-Voice-Assistant/repos"

responses = {
    "pluginInstall": [],
    "pluginUninstall": [],
    "pluginInit": [],
    "pluginNeedsInit": [],
}


def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.
    If the error is due to an access error (read only file)
        it attempts to add write permission and then retries.
    If the error is for another reason it re-raises the error.
    """
    import stat

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        # Try to change the permission of the file/folder
        os.chmod(path, stat.S_IWUSR)
        # Retry
        func(path)
    else:
        # Raise the error again
        raise


def handle_plugin(intent, entities):
    plugin = entities.get("plugin", [{}]).get("value", None)

    if not plugin:
        return  # error

    if intent == "install":
        log("here")
        data = requests.get(GITHUB_URL)
        data = data.json()

        log(data)

        names = []
        for item in data:
            log(item)
            name = item["name"]
            if name.startswith("plugin_"):
                names.append(name.replace("plugin_", "", 1))

        closest = similarFromList(plugin, names)

        for plugin_name in os.listdir(PLUGIN_PATH):
            if plugin_name == closest:
                return print("ALREADY INSTALLED!!!")

        plugin = None
        for item in data:
            if item["name"] == "plugin_" + closest:
                plugin = item

        log(plugin)
        name = plugin["name"].replace("plugin_", "")

        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    plugin["git_url"].replace("git://", "https://"),
                    os.path.join(PLUGIN_PATH, name),
                ],
                check=True,
            )

            print(f"Repository cloned to {PLUGIN_PATH}")
            # Run initialization
            from app.extensions import extensions

            log(f"disabling plugin {name}")

            extensions.plugin_manager.add_plugin_disabled(name)

            extensions.plugin_manager.load_plugins()
        except subprocess.CalledProcessError:
            print("Error cloning the repository.")

        # CHECK IF REQUIRES SETUP ----------------------

        plugin = extensions.plugin_manager.get_plugin_by_name(name)

        # if hasattr(plugin, "initialize"):
        #     # Can Be initialized
        #     value = getYesorNo()
        #     if value:
        #         pass
    elif intent == "uninstall":
        plugins = []
        for plugin_name in os.listdir(PLUGIN_PATH):
            log(plugin_name)
            plugins.append(plugin_name)

        closest = similarFromList(plugin, plugins)

        if not closest:
            return log("Not installed!!!!")

        newPath = os.path.join(PLUGIN_PATH, closest)

        shutil.rmtree(newPath, ignore_errors=False, onerror=onerror)

        from app.extensions import extensions

        extensions.plugin_manager.load_plugins()

        pass
    elif intent == "init":
        plugins = []
        for plugin_name in os.listdir(PLUGIN_PATH):
            log(plugin_name)
            plugins.append(plugin_name)

        closest = similarFromList(plugin, plugins)

        from app.extensions import extensions

        extensions.plugin_manager.runInit(closest)

        log("pIinit")
        pass
