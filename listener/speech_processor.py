"""
This module handles the speech to text part of the code
"""

from PySide6.QtCore import QObject, Signal, QThread

import sounddevice
import numpy as np

from .transcriber import Transcriber

# Audio input parameters
SAMPLE_RATE = 16000
BLOCK_SIZE = int(0.1 * SAMPLE_RATE)
CHANNEL_TYPE = 1
MAX_AUDIO_CHUNKS = 4
TRANSFER_RATE = 16

SILENCE_RMS_THRESHOLD = 0.008
SILENCE_BLOCK_COUNT = 15


class ProcessSpeech(QObject):
    updated_text = Signal(str)
    rms_value = Signal(float)
    end_of_transcription = Signal()

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.transcriber = Transcriber(self.config["listener_params"])

    def process_input_stream(self):
        speech_started = False
        silence_block_count = 0

        input_stream = sounddevice.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=CHANNEL_TYPE,
        )

        self.transcriber.reset_stream()

        with input_stream as stream:
            stream.stop()
            stream.start()

            while not QThread.currentThread().isInterruptionRequested():

                audio_data, _ = stream.read(BLOCK_SIZE)
                audio_data = audio_data.reshape(-1)

                voice_input = self.transcriber.speech_to_text(
                    audio_data, sample_rate=SAMPLE_RATE
                ).lower()

                # Logic to detect prolonged silence and control the halo
                audio_rms_energy = np.sqrt(np.mean(audio_data**2))

                if audio_rms_energy > SILENCE_RMS_THRESHOLD:
                    silence_block_count = 0
                    if not speech_started:
                        speech_started = True
                else:
                    if speech_started:
                        silence_block_count += 1

                self.rms_value.emit(audio_rms_energy)

                if silence_block_count >= SILENCE_BLOCK_COUNT:
                    self.end_of_transcription.emit()

                self.updated_text.emit(voice_input)
