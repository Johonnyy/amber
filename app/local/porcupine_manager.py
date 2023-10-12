import pvporcupine
import pyaudio
import struct
import platform
import datetime
import os
from .speech_recognition_manager import startRecording
from .text_to_speech import generateAudio
from app.functions import *
import sys


arch = platform.machine()

base_dir = None

if frozen():
    base_dir = get_base_dir()
else:
    base_dir = os.path.dirname(get_base_dir())

if arch == "AMD64":
    location = os.path.join(base_dir, "custom_wake_words", "windows")
    keyword_paths = [
        os.path.join(location, "hey-amber_en_windows_v2_2_0.ppn"),
        os.path.join(location, "yo-amber_en_windows_v2_2_0.ppn"),
        os.path.join(location, "Unmute_en_windows_v2_2_0.ppn"),
    ]
else:
    location = os.path.join(base_dir, "custom_wake_words", "linux")
    keyword_paths = [
        os.path.join(location, "hey-amber_en_linux_v2_2_0.ppn"),
        os.path.join(location, "yo-amber_en_linux_v2_2_0.ppn"),
        os.path.join(location, "Unmute_en_linux_v2_2_0.ppn"),
    ]


@prevent_plugin_access
def get_next_audio_frame(audio_stream, porcupine):
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    return pcm


@prevent_plugin_access
def startListening():
    porcupine = pvporcupine.create(
        access_key=getConfig()["picovoiceKey"],
        keyword_paths=keyword_paths,
    )

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
    )

    global current_state
    log("started listening")
    while True:
        audio_frame = get_next_audio_frame(audio_stream, porcupine)
        keyword_index = porcupine.process(audio_frame)
        if keyword_index == 0 or keyword_index == 1:
            from .main import localDevice

            if localDevice.muted:
                continue

            log("detected wake word")

            # Update the state to RECORDING
            startRecording()
            from .main import localDevice

            localDevice.api.createNewSession()

        elif keyword_index == 2:
            log("detected unmute command")
            from .main import localDevice

            if localDevice.muted:
                localDevice.muted = False
                generateAudio("Okay, I've been unmuted.")
