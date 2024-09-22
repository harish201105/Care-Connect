import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QStyle, QApplication, QMenuBar, \
    QDialog

from utils import SerialCommunicator


class ConnectCamFollower(QDialog):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        # self.root_window = root_window
        self.setWindowTitle("Connect to Cam Follower")
        self.setStyleSheet("background-color: #E2D1F9;")
        self.setFixedSize(400, 200)

        # Create widgets
        self._render_label("Com Ports")
        self._render_combo_box()
        self._render_button("Connect")

        # Connect action listeners
        self.combo_box.currentTextChanged.connect(self._on_combo_box_changed)
        self.button.clicked.connect(self._on_button_clicked)

        # Create layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.label)
        # layout.addWidget(self.combo_box)
        # layout.addWidget(self.button)
        # self.setLayout(layout)

        # Position and size widgets
        self.label.move(50, 70)
        self.label.setFixedSize(100, 30)

        self.combo_box.move(160, 70)
        self.combo_box.setFixedSize(200, 30)

        self.button.move(130, 130)
        self.button.setFixedSize(160, 30)

        self.show()

    def _render_label(self, text):
        self.label = QLabel(text, self)
        self.label.setStyleSheet("background-color: green; color: white;font-size: 15px;")
        self.label.setAlignment(Qt.AlignCenter)
        return self.label

    def _render_combo_box(self):
        self.combo_box = QComboBox(self)
        # Populate the combo box with available COM ports
        cancel_icon = self.style().standardIcon(QStyle.SP_TitleBarCloseButton)
        self.combo_box.addItem(cancel_icon, "NONE")
        ports = SerialCommunicator.get_all_comports()
        self.combo_box.addItems(ports)
        return self.combo_box

    def _render_button(self, text):
        self.button = QPushButton(text, self)
        self.button.setStyleSheet("background-color: green; color: white;")
        self._set_button_enabled(False)

    def _set_button_enabled(self, enabled: bool):
        if enabled:
            self.button.setStyleSheet("background-color: green;"
                                      "color: white;"
                                      "font-size: 20px;")
            self.button.setEnabled(True)
        else:
            self.button.setStyleSheet("background-color: gray;"
                                      "color: white;"
                                      "font-size: 20px;")
            self.button.setEnabled(False)

    def _on_combo_box_changed(self, text):
        if text == "NONE":
            self._set_button_enabled(False)
        else:
            self._set_button_enabled(True)

    def _on_button_clicked(self):
        self.root_window.serial_communicator = SerialCommunicator(self.combo_box.currentText())
        self.root_window.follow_cam = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnectCamFollower()
    sys.exit(app.exec_())

