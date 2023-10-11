class BaseDevice:
    def __init__(self, name, id, description, version):
        self.name = name
        self.id = id
        self.description = description
        self.version = version

    def start():
        """Start listening for messages from user"""
        raise NotImplementedError
