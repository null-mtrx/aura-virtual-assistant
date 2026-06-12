"""
This module handles the animation frame that plays the bead when the user is speaking
"""

from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPainter, QPen, QBrush, QColor
from PySide6.QtCore import QPoint, QSize, Property

import numpy as np

DIMS = 200

ANIMATION_DURATION_FORWARD = 150
ANIMATION_DURATION_BACKWARD = 874

MIN_BEAD_RAD = 15
MAX_BEAD_RAD = 40

BEAD_THICKNESS = 4
BEAD_PRIMARY_COLOR = "#49b6d3"
BEAD_SECONDARY_COLOR = "#0a416e"


class BeadFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.bead_radius = MIN_BEAD_RAD
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @Property(float)
    def bead_rad(self):
        return self.bead_radius

    @bead_rad.setter
    def bead_rad(self, val):
        self.bead_radius = val
        self.update()

    def minimumSizeHint(self):
        return QSize(300, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(QColor(BEAD_PRIMARY_COLOR))
        painter.setPen(pen)

        brush = QBrush(QColor(BEAD_PRIMARY_COLOR))
        painter.setBrush(brush)

        center = QPoint(self.width() / 2, self.height() / 2)

        painter.drawEllipse(center, 2 * self.bead_radius, 2 * self.bead_radius)
        painter.end()


class AnimFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.anim_frame_layout = QVBoxLayout(self)
        self.bead = BeadFrame()
        self.anim_frame_layout.addWidget(self.bead)

    def animate_bead(self, block_rms):
        bead_rad_changed = 20 * np.sqrt(block_rms) + MIN_BEAD_RAD

        if bead_rad_changed > MAX_BEAD_RAD:
            bead_rad_changed = MAX_BEAD_RAD

        setattr(self.bead, "bead_rad", bead_rad_changed)
