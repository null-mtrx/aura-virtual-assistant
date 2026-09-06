"""
import json
from listener.speech_processor import ProcessSpeech

with open("/home/w4sp/Projects/Voice-Assistant/config.json", "r") as file:
    config = json.load(file)

ProcessSpeech(config).process_input_stream()
"""

from PySide6.QtWidgets import QApplication
from window import MainWindow
import sys

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = MainWindow()
window.show()
app.exec()
