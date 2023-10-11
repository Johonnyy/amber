import azure.cognitiveservices.speech as speechsdk
import time
from app.functions import log, getConfig
from .text_to_speech import generateAudio


def startRecording(ttl=10, skip=False):
    from .main import localDevice

    localDevice.event("startListening")
    config = getConfig()
    speech_config = speechsdk.SpeechConfig(
        subscription=config["azureKey"], region=config["speech"]["region"]
    )
    speech_config.speech_recognition_language = "en-US"
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    start_time = time.time()
    while time.time() - start_time < ttl:
        log("Speak into your microphone.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            if any(
                punctuation in speech_recognition_result.text
                for punctuation in [".", "?", "!"]
            ):
                break
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            log(
                "No speech could be recognized: {}".format(
                    speech_recognition_result.no_match_details
                )
            )
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            log("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                log("Error details: {}".format(cancellation_details.error_details))
                log("Did you set the speech resource key and region values?")
    log("finished")
    result = speech_recognition_result.text

    localDevice.event("stopListening")

    if skip == True:
        return result

    log(result)
    intentResult = localDevice.api.sendInput(result)
    log(intentResult)

    generateAudio(intentResult)
