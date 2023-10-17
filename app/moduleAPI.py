from app.functions import log, similar, similarFromList

# from app.assistant.response_manager import generate_name, generate_error
# from app.assistant.text_to_speech import generateAudio
# from app.assistant.speech_recognition_manager import listenForValue


def getCredential(
    type: str = None,
    moduleName: str = None,
    functionName: str = None,
    credential: str = None,
):
    from app.extensions import extensions

    return extensions.module_manager.getInput(
        type, moduleName, functionName, credential
    )
