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

PRIMARY_MIN_BEAD_RAD = 15
PRIMARY_MAX_BEAD_RAD = 30

SECONDARY_MIN_BEAD_RAD = 25
SECONDARY_MAX_BEAD_RAD = 50

PRIMARY_BEAD_COLOR = "#49b6d3"
SECONDARY_BEAD_COLOR = "#0a416e"


class BeadFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.primary_bead_radius = PRIMARY_MIN_BEAD_RAD
        self.secondary_bead_radius = SECONDARY_MIN_BEAD_RAD
        self.setMaximumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    @Property(float)
    def primary_bead_rad(self):
        return self.primary_bead_radius

    @primary_bead_rad.setter
    def primary_bead_rad(self, val):
        self.primary_bead_radius = val
        self.update()

    @Property(float)
    def secondary_bead_rad(self):
        return self.secondary_bead_radius

    @primary_bead_rad.setter
    def secondary_bead_rad(self, val):
        self.secondary_bead_radius = val
        self.update()

    def minimumSizeHint(self):
        return QSize(300, 300)

    def paintEvent(self, event):
        painter = QPainter(self)
        center = QPoint(self.width() / 2, self.height() / 2)

        primary_pen = QPen(QColor(PRIMARY_BEAD_COLOR))
        primary_brush = QBrush(QColor(PRIMARY_BEAD_COLOR))
        secondary_pen = QPen(QColor(SECONDARY_BEAD_COLOR))
        secondary_brush = QBrush(QColor(SECONDARY_BEAD_COLOR))

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(secondary_pen)
        painter.setBrush(secondary_brush)

        painter.drawEllipse(
            center, 2 * self.secondary_bead_radius, 2 * self.secondary_bead_radius
        )

        painter.setPen(primary_pen)
        painter.setBrush(primary_brush)

        painter.drawEllipse(
            center, 2 * self.primary_bead_radius, 2 * self.primary_bead_radius
        )
        painter.end()


class AnimFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.anim_frame_layout = QVBoxLayout(self)
        self.bead = BeadFrame()
        self.anim_frame_layout.addWidget(self.bead)

    def animate_beads(self, block_rms):
        new_primary_bead_rad = 20 * np.sqrt(block_rms) + PRIMARY_MIN_BEAD_RAD
        new_secondary_bead_rad = 20 * np.sqrt(block_rms) + SECONDARY_MIN_BEAD_RAD

        if new_primary_bead_rad > PRIMARY_MAX_BEAD_RAD:
            new_primary_bead_rad = PRIMARY_MAX_BEAD_RAD

        if new_secondary_bead_rad > SECONDARY_MAX_BEAD_RAD:
            new_secondary_bead_rad = SECONDARY_MAX_BEAD_RAD

        setattr(self.bead, "primary_bead_rad", new_primary_bead_rad)
        setattr(self.bead, "secondary_bead_rad", new_secondary_bead_rad)
