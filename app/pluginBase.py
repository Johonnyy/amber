class BasePlugin:
    def __init__(
        self,
        displayName,
        name,
        description,
        version,
        category,
        configOptions=[],
        dependencies=[],
    ):
        self.displayName = displayName
        self.name = name
        self.description = description
        self.version = version
        self.category = category
        self.configOptions = configOptions
        self.dependencies = dependencies

    def can_handle(self, intent):
        """Check if the plugin can handle the given intent."""
        raise NotImplementedError

    def handle(self, intent, entities):
        """Handle the intent and entities."""
        raise NotImplementedError
