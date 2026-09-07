from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

import json
import os


class ControlFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.control_frame_layout = QHBoxLayout()
        self.build_ui()
        self.setLayout(self.control_frame_layout)

    def wifi_loaded(self):
        net_path = "/sys/class/net"
        try:
            data = os.listdir(net_path)
            interfaces = [i for i in data if i.startswith("wlan", "wlp")]

            for interface in interfaces:
                operstate_file = os.path.join(net_path, interface, "operstate")
                if os.path.exists(operstate_file):
                    with open(operstate_file, "r") as file:
                        data = file.read().strip()
                    if data == "up":
                        return True
            else:
                return False
        except:
            return False

    def build_ui(self):
        with open("config.json", "r") as file:
            data = json.load(file)

        mic_file_path = data["ui"]["mic-icon"]
        setting_file_path = data["ui"]["setting-icon"]

        if self.wifi_loaded:
            wifi_loaded_icon = data["ui"]["wifi-up-icon"]
        else:
            wifi_loaded_icon = data["ui"]["wifi-down-icon"]

        self.input_button = QPushButton()
        self.input_button.setIcon(QIcon(mic_file_path))
        self.input_button.setIconSize(QSize(24, 24))
        self.input_button.setMaximumSize(QSize(30, 40))

        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(setting_file_path))
        self.settings_button.setIconSize(QSize(24, 24))

        self.wifi_button = QPushButton()
        self.wifi_button.setIcon(QIcon(wifi_loaded_icon))
        self.wifi_button.setIconSize(QSize(24, 24))

        self.control_frame_layout.addWidget(self.wifi_button)
        self.control_frame_layout.addSpacerItem(
            QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.control_frame_layout.addWidget(self.input_button)
        self.control_frame_layout.addSpacerItem(
            QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        )
        self.control_frame_layout.addWidget(self.settings_button)
