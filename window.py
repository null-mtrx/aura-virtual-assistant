"""
Builds the main window for the UI
"""

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QThread, QCoreApplication, QTimer, Signal
from PySide6.QtCore import Qt

from ui.anim_frame import AnimFrame
from ui.io_frame import IOFrame
from ui.control_frame import ControlFrame
from ui.op_frame import OPFrame

from listener.speech_processor import ProcessSpeech
from speaker.speech_engine import SpeechEngine

from agent.agent_module import AgentInterface

import json

with open("/home/w4sp/Projects/Voice-Assistant/config.json", "r") as file:
    config = json.load(file)


with open("src/ui/app.qss", "r") as file:
    style = file.read()


class MainWindow(QMainWindow):
    ai_query = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Assistant")
        self.setFixedSize(300, 660)
        self.setStyleSheet(style)
        self.processor = ProcessSpeech(config=config)
        self.speaker = SpeechEngine(config=config["speaker_params"])

        self.agent = AgentInterface()
        self.agent_thread = QThread()
        self.agent.moveToThread(self.agent_thread)
        self.ai_query.connect(self.agent.respond_to_query)

        self.agent_thread.start()
        self.agent.output_tokens.connect(
            self.play_output, Qt.ConnectionType.QueuedConnection
        )

        self.build_ui()

    def build_ui(self):
        self.central_widget = QWidget()
        self.widget_layout = QVBoxLayout(self.central_widget)

        self.anim_frame = AnimFrame()
        self.widget_layout.addWidget(self.anim_frame)

        self.op_frame = OPFrame()
        self.widget_layout.addWidget(self.op_frame)

        self.io_frame = IOFrame()
        self.widget_layout.addWidget(self.io_frame)

        self.control_frame = ControlFrame()
        self.control_frame.input_button.clicked.connect(self.start_speech_input)
        self.widget_layout.addWidget(self.control_frame)

        self.setCentralWidget(self.central_widget)

    def start_speech_input(self):
        self.io_frame.clear_label()
        self.op_frame.clear_label()

        self.audio_thread = QThread()
        self.processor.moveToThread(self.audio_thread)
        self.audio_thread.started.connect(self.processor.process_input_stream)
        self.processor.updated_text.connect(self.io_frame.update_label_text)
        self.processor.rms_value.connect(
            lambda block_rms: self.anim_frame.animate_beads(block_rms)
        )
        self.processor.end_of_transcription.connect(self.stop_speech_input)
        self.audio_thread.finished.connect(self.audio_thread.deleteLater)

        self.audio_thread.start()

    def retrieve_query(self):
        text = self.io_frame.label.text()

        if self.control_frame.input_button.isEnabled() and text:
            self.control_frame.input_button.setDisabled(True)
            self.ai_query.emit(self.io_frame.label.text())

    def play_output(self, text: str):
        self.op_frame.update_label_text(text)
        self.speaker.duration.connect(self.anim_frame.start_output_animation)
        self.speaker.speak(text)
        self.control_frame.input_button.setEnabled(True)

    def stop_speech_input(self):
        self.main_thread = QCoreApplication.instance().thread()

        if self.audio_thread.isRunning() and hasattr(self, "audio_thread"):
            self.audio_thread.requestInterruption()
            self.audio_thread.quit()
            self.audio_thread.wait()

        QTimer.singleShot(50, self.retrieve_query)
