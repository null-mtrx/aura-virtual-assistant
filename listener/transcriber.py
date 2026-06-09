"""
This module is responsible for transcribing the speech data into text
"""

import sherpa_onnx
import pathlib
import json

NUM_THREADS = 2
SAMPLE_RATE = 16000
FEATURE_DIM = 80

RULE1_MIN_TRAILING_SILENCE = 2.4
RULE2_MIN_TRAILING_SILENCE = 1.2
RULE3_MIN_UTTERANCE_LENGTH = 300

with open("/home/w4sp/Projects/Voice-Assistant/config.json", "r") as file:
    config = json.load(file)


class Transcriber:
    def __init__(self):
        self.tokens = config["listener_params"]["tokens"]
        self.encoder = config["listener_params"]["encoder_path"]
        self.decoder = config["listener_params"]["decoder_path"]
        self.joiner = config["listener_params"]["joiner_path"]

        self.recogniser = sherpa_onnx.OnlineRecognizer.from_transducer(
            tokens=self.tokens,
            encoder=self.encoder,
            decoder=self.decoder,
            joiner=self.joiner,
            num_threads=NUM_THREADS,
            sample_rate=SAMPLE_RATE,
            feature_dim=FEATURE_DIM,
            rule1_min_trailing_silence=RULE1_MIN_TRAILING_SILENCE,
            rule2_min_trailing_silence=RULE2_MIN_TRAILING_SILENCE,
            rule3_min_utterance_length=RULE3_MIN_UTTERANCE_LENGTH,
            decoding_method="greedy_search",
            provider="cpu",
        )
        self.stream = self.recogniser.create_stream()
        self.display = sherpa_onnx.Display()

    def speech_to_text(self, data, sample_rate):
        self.stream.accept_waveform(sample_rate, data)

        while self.recogniser.is_ready(self.stream):
            self.recogniser.decode_stream(self.stream)

        result = self.recogniser.get_result(self.stream)
        end_of_speech = self.recogniser.is_endpoint(self.stream)

        print(result, end="")
        if end_of_speech:
            if result:
                print(result)

            self.recogniser.reset(self.stream)
