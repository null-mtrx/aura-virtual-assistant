"""
This module handles the speech to text part of the code
"""

from PySide6.QtCore import QObject, Signal

import sounddevice
import numpy as np

from .transcriber import Transcriber

# Audio input parameters
SAMPLE_RATE = 16000
BLOCK_SIZE = int(0.1 * SAMPLE_RATE)
CHANNEL_TYPE = 1
MAX_AUDIO_CHUNKS = 4

SILENCE_RMS_THRESHOLD = 0.009
SILENCE_BLOCK_COUNT = 7


class ProcessSpeech(QObject):
    updated_text = Signal(str)

    def __init__(self, config):
        super().__init__()
        self.transcriber = Transcriber(config["listener_params"])
        self.is_running = True

    def process_input_stream(self):
        input_stream = sounddevice.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=CHANNEL_TYPE,
        )

        print("Speech recognition starting now")
        with input_stream as stream:
            while self.is_running:
                audio_data, _ = stream.read(BLOCK_SIZE)
                audio_data = audio_data.reshape(-1)

                voice_input = self.transcriber.speech_to_text(
                    audio_data, sample_rate=SAMPLE_RATE
                ).lower()
                self.updated_text.emit(voice_input)
