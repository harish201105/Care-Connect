import sys

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QDialog


class AddCamWindow(QDialog):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window

        self.setWindowTitle("Add Camera")
        self.setStyleSheet("background-color: #E2D1F9;")
        self.setGeometry(100, 100, 300, 350)
        self.setFixedSize(300, 450)

        self.__render_camera_name_field()
        self.__render_protocol_field()
        self.__render_url_field()
        self.__render_port_field()
        self.__render_stream_field()
        self.__render_add_camera_button()

        vbox = QVBoxLayout()
        vbox.addWidget(self.camera_name_label)
        vbox.addWidget(self.camera_name_entry)
        vbox.addWidget(self.protocol_label)
        vbox.addWidget(self.protocol_entry)
        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_entry)
        vbox.addWidget(self.port_label)
        vbox.addWidget(self.port_entry)
        vbox.addWidget(self.stream_label)
        vbox.addWidget(self.stream_entry)
        vbox.addWidget(self.add_camera_button)

        self.setLayout(vbox)

        self.show()

    def __render_camera_name_field(self):
        self.camera_name_label_layout = QHBoxLayout()
        self.camera_name_label = QLabel("Camera Name:")
        self.camera_name_entry = QLineEdit()
        self.camera_name_label_layout.addWidget(self.camera_name_label)
        self.camera_name_label_layout.addWidget(self.camera_name_entry)

    def __render_protocol_field(self):
        self.protocol_label_layout = QHBoxLayout()
        self.protocol_label = QLabel("Protocol:")
        self.protocol_entry = QLineEdit()
        self.protocol_label_layout.addWidget(self.protocol_label)
        self.protocol_label_layout.addWidget(self.protocol_entry)

    def __render_url_field(self):
        self.url_label_layout = QHBoxLayout()
        self.url_label = QLabel("IP Address:")
        self.url_entry = QLineEdit()
        self.url_label_layout.addWidget(self.url_label)
        self.url_label_layout.addWidget(self.url_entry)

    def __render_port_field(self):
        self.port_label_layout = QHBoxLayout()
        self.port_label = QLabel("Port:")
        self.port_entry = QLineEdit()
        self.port_label_layout.addWidget(self.port_label)
        self.port_label_layout.addWidget(self.port_entry)

    def __render_stream_field(self):
        self.stream_label_layout = QHBoxLayout()
        self.stream_label = QLabel("Stream:")
        self.stream_entry = QLineEdit()
        self.stream_label_layout.addWidget(self.stream_label)
        self.stream_label_layout.addWidget(self.stream_entry)

    def __render_add_camera_button(self):
        self.add_camera_button_layout = QHBoxLayout()
        self.add_camera_button = QPushButton("Add Camera")
        self.add_camera_button.clicked.connect(self.__add_camera_action)
        self.add_camera_button_layout.addWidget(self.add_camera_button)

    def __add_camera_action(self):
        cam_name = self.camera_name_entry.text().strip()
        protocol = self.protocol_entry.text().strip()
        ip = self.url_entry.text().strip()
        port = self.port_entry.text().strip()
        stream = self.stream_entry.text().strip()

        cam_url = f"{protocol}://{ip}:{port}/{stream}"

        self.parent_window.add_cam(cam_url, cam_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddCamWindow(None)  # Pass the parent window if needed
    window.show()
    sys.exit(app.exec_())
