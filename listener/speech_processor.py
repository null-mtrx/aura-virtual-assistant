"""
This module handles the speech to text part of the code
"""

import sounddevice
import numpy as np
import queue

# Audio input parameters
SAMPLE_RATE = 16_000
BLOCK_SIZE = 4096
CHANNEL_TYPE = 1
MAX_AUDIO_CHUNKS = 4

SILENCE_RMS_THRESHOLD = 0.009
SILENCE_BLOCK_COUNT = 7


class ProcessSpeech:
    def __init__(self):
        self.audio_queue = queue.Queue()

    def process_input_stream(self):
        audio_stack = []
        audio_chunk_count = 0
        speech_started = False
        silence_block_count = 0

        def callback(indata, frames, time, status):
            self.audio_queue.put(indata)

        input_stream = sounddevice.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=CHANNEL_TYPE,
            callback=callback,
        )

        with input_stream:
            while True:
                in_data = self.audio_queue.get()
                audio_data = np.frombuffer(in_data, dtype=np.float32)
                audio_rms = np.sqrt(np.mean(audio_data**2))

                # for debugging purposes
                print("RMS value", audio_rms)
                print("Silent Block Count", silence_block_count)

                if audio_rms > SILENCE_RMS_THRESHOLD:
                    silence_block_count = 0
                    if not speech_started:
                        speech_started = True
                else:
                    if speech_started:
                        silence_block_count += 1

                audio_stack.append(audio_data)
                audio_chunk_count += 1

                if audio_chunk_count == MAX_AUDIO_CHUNKS:
                    audio_chunk = np.concatenate(audio_stack)
                    print(audio_chunk.shape)

                    for i in range(3):
                        audio_stack.pop(0)

                    audio_chunk_count = 1

                if silence_block_count >= SILENCE_BLOCK_COUNT:
                    break
