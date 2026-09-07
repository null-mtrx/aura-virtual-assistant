from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QPainter, QIcon
from PySide6.QtSvg import QSvgRenderer

import json


class ControlFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.control_frame_layout = QHBoxLayout()
        self.build_ui()
        self.setLayout(self.control_frame_layout)

    def build_ui(self):
        with open("config.json", "r") as file:
            data = json.load(file)

        mic_file_path = data["ui"]["mic-icon"]

        self.input_button = QPushButton()
        self.input_button.setIcon(QIcon(mic_file_path))
        self.control_frame_layout.addWidget(self.input_button)
