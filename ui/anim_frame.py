"""
This module handles the animation frame that plays the halo when the user is speaking
"""

from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import QPoint, QSize

PIXMAP_SIZE = 300
HALO_RAD = 20
HALO_THICKNESS = 1
HALO_BORDER_COLOR = "#e0d9ba"


class AnimFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def sizeHint(self):
        return QSize(200, 200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(QColor(HALO_BORDER_COLOR))
        painter.setPen(pen)

        center = QPoint(self.width() / 2, self.height() / 2)

        painter.drawEllipse(center, 2 * HALO_RAD, 2 * HALO_RAD)
        painter.end()
