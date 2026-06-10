"""
This module handles the io area for the voice assistant
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Signal


class IOFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.frame_layout = QVBoxLayout()
        self._build_ui()

        self.setLayout(self.frame_layout)

    def _build_ui(self):
        self.label = QLabel("Text here")
        self.label.setWordWrap(True)
        self.frame_layout.addWidget(self.label)

    def update_label_text(self, voice_input):
        self.label.setText(voice_input)
