"""
This module handles the io area for the voice assistant
"""

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal


class IOFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.frame_layout = QVBoxLayout()
        self._build_ui()
        self.setFixedHeight(75)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setLayout(self.frame_layout)

    def _build_ui(self):
        self.label = QLabel("Start speaking here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)
        self.frame_layout.addWidget(self.label)

    def update_label_text(self, voice_input):
        self.label.setText(voice_input)

    def clear_label(self):
        self.label.setText("")
