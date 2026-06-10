from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton


class ControlFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.control_frame_layout = QHBoxLayout()
        self.build_ui()
        self.setLayout(self.control_frame_layout)

    def build_ui(self):
        self.input_button = QPushButton("Speak")
        self.control_frame_layout.addWidget(self.input_button)
