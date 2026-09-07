from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
    QGraphicsOpacityEffect,
)
from PySide6.QtCore import Signal, QPropertyAnimation, QEasingCurve, Qt


class OPFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.frame_layout = QVBoxLayout()
        self._build_ui()
        self.setMinimumHeight(260)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding
        )

        self.setLayout(self.frame_layout)

    def _build_ui(self):
        self.title_label = QLabel("<h1>Hi I'm Aura</h1><br>How can I help you today")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title_label.setObjectName("title")

        self.label = QLabel("")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.frame_layout.addWidget(self.label)
        self.frame_layout.addWidget(self.title_label)

    def update_label_text(self, voice_input):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.0)

        self.label.setText(voice_input)
        self.label.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.animation.start()

    def clear_label(self):
        self.title_label.setText("")
        self.label.setText("")
