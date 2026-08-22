from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Signal


class OPFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.frame_layout = QVBoxLayout()
        self._build_ui()
        self.setMinimumHeight(240)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )

        self.setLayout(self.frame_layout)

    def _build_ui(self):
        self.label = QLabel("Text here")
        self.label.setWordWrap(True)
        self.frame_layout.addWidget(self.label)

    def update_label_text(self, voice_input):
        self.label.setText(voice_input)

    def clear_label(self):
        self.label.setText("")
