import azure.cognitiveservices.speech as speechsdk
import yaml
import os
import datetime
from app.functions import *


@prevent_plugin_access
def generateAudio(text):
    config = getConfig()

    speech_config = speechsdk.SpeechConfig(
        subscription=config["azureKey"], region=config["speech"]["region"]
    )
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_config.speech_synthesis_voice_name = config["speech"]["voice"]

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    log("started generating audio")

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if (
        speech_synthesis_result.reason
        == speechsdk.ResultReason.SynthesizingAudioCompleted
    ):
        log("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        log("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                log("Error details: {}".format(cancellation_details.error_details))
                log("Did you set the speech resource key and region values?")

    log("generated, now playing")

    log("played")
    log()
