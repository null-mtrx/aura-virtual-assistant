"""
This module handles the speech to text part of the code
"""

import sounddevice
import numpy as np
import queue

from .transcriber import Transcriber

# Audio input parameters
SAMPLE_RATE = 16000
BLOCK_SIZE = int(0.1 * SAMPLE_RATE)
CHANNEL_TYPE = 1
MAX_AUDIO_CHUNKS = 4

SILENCE_RMS_THRESHOLD = 0.009
SILENCE_BLOCK_COUNT = 7


class ProcessSpeech:
    def __init__(self):
        self.transcriber = Transcriber()

    def process_input_stream(self):
        input_stream = sounddevice.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=CHANNEL_TYPE,
        )

        print("Speech recognition starting now")
        with input_stream as stream:
            while True:
                audio_data, _ = stream.read(BLOCK_SIZE)
                audio_data = audio_data.reshape(-1)

                self.transcriber.speech_to_text(audio_data, sample_rate=SAMPLE_RATE)
