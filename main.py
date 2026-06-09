import json
from listener.speech_processor import ProcessSpeech

with open("/home/w4sp/Projects/Voice-Assistant/config.json", "r") as file:
    config = json.load(file)

ProcessSpeech(config).process_input_stream()
