class DeviceAPI:
    def __init__(self):
        from app.extensions import extensions

        self.openaiManager = extensions.openai_manager

    def createNewSession(self):
        self.openaiManager.newSession()

    def sendInput(self, input):
        return self.openaiManager.newUserMessage(input)

    def getMissingEntity(self, text, deviceId, sessionId):
        # print("getMissingEntity")
        # instance = extensions.device_manager.get_device_by_id(deviceId)
        # value = instance.getEntity(text)
        # print(sessionId)
        # response = None  # detect_intention(value, sessionId)
        # return response
        pass
