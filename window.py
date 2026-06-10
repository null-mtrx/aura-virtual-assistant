"""
Builds the main window for the UI
"""

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QThread
from ui.io_frame import IOFrame
from ui.control_frame import ControlFrame

from listener.speech_processor import ProcessSpeech
import json

with open("/home/w4sp/Projects/Voice-Assistant/config.json", "r") as file:
    config = json.load(file)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Assistant")
        self.setFixedSize(300, 660)
        self.processor = ProcessSpeech(config=config)
        self.build_ui()

    def build_ui(self):
        self.central_widget = QWidget()
        self.widget_layout = QVBoxLayout(self.central_widget)

        self.io_frame = IOFrame()
        self.widget_layout.addWidget(self.io_frame)

        self.control_frame = ControlFrame()
        self.control_frame.input_button.clicked.connect(self.start_speech_input)
        self.widget_layout.addWidget(self.control_frame)

        self.setCentralWidget(self.central_widget)

    def start_speech_input(self):
        self.audio_thread = QThread()
        self.processor.moveToThread(self.audio_thread)
        self.audio_thread.started.connect(self.processor.process_input_stream)
        self.processor.updated_text.connect(self.io_frame.update_label_text)
        self.processor.end_of_transcription.connect(self.stop_speech_input)
        self.audio_thread.finished.connect(self.audio_thread.deleteLater)

        self.audio_thread.start()

    def stop_speech_input(self):
        if self.audio_thread.isRunning():
            self.audio_thread.requestInterruption()
            self.audio_thread.quit()
            self.io_frame.clear_label()
