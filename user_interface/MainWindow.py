import threading
import time

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QPushButton, QStyle, QAction
from PyQt5.QtCore import Qt


from computer_vision import CameraManager, Camera
from computer_vision import ActionTracker, ActionClassifier

from game_interface import GameController, ZeldaAdaptor
from utils import VoiceAssistant, SerialCommunicator

from user_interface import ConnectCamFollower, NoCodeUi, AddCamWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.action_tracker = ActionTracker()
        self.action_classifier = ActionClassifier()
        self.serial_communicator = SerialCommunicator(port="COM5")

        # Create a window with title Gesture GamePad VR, Size 800x600 and background color #E2D1F9
        self.setWindowTitle("Gesture GamePad VR")
        self.setFixedSize(700, 720)
        # self.setGeometry(100, 100, 700, 720)
        self.setStyleSheet("background-color: #E2D1F9;")

        self.follow_cam = False
        self._started = False
        self._game_adapters = {"Zelda": ZeldaAdaptor}
        self._game_adaptor = None
        self._game_controller = None

        self._voice_assistant = VoiceAssistant()

        # self._start_bg_loop()
        # self.__render_img_text_label()
        # self._set_bg()
        self._render_menu_bar()
        self._render_image_label()
        self._render_action_button()
        self._render_cam_select_label()
        self._render_game_select_label()
        self._render_select_cam_combobox()
        self._render_select_game_combobox()

        self._create_default_camera_manager()
        self._start_process_loop()
        # threading.Thread(target=self._start_bg_loop, daemon=True).start()

    def closeEvent(self, event):
        # pass
        self.serial_communicator.send("end\n")

    def _render_image_label(self):
        # Make a 500x500 Image label
        self._image_label = QLabel(self)
        self._image_label.setFixedSize(500, 500)
        self._image_label.move(100, 50)
        self._image_label.setStyleSheet("background-color: black;"
                                        "color: white;"
                                        "font-size: 20px;"
                                        "border: 1px solid black;")
        self._image_label.setAlignment(Qt.AlignCenter)
        self._image_label.setText("No Camera Selected")

    def _render_select_cam_combobox(self):
        # Make a combo box with the last element as Add Cam
        self._select_cam_combobox = QComboBox(self)
        self._select_cam_combobox.move(210, 675)
        self._select_cam_combobox.setFixedSize(150, 30)

        cancel_icon = self.style().standardIcon(QStyle.SP_TitleBarCloseButton)
        self._select_cam_combobox.addItem(cancel_icon, "NONE")

        self._select_cam_combobox.activated.connect(self._on_select_cam_activated)

    def _render_select_game_combobox(self):
        # Make a combo box to select the game
        self._select_game_combobox = QComboBox(self)
        self._select_game_combobox.move(420, 675)
        self._select_game_combobox.setFixedSize(150, 30)

        cancel_icon = self.style().standardIcon(QStyle.SP_TitleBarCloseButton)
        self._select_game_combobox.addItem(cancel_icon, "NONE")
        self._select_game_combobox.addItems(self._game_adapters.keys())

        self._select_game_combobox.activated.connect(self._on_select_game_activated)

    def _render_action_button(self):
        # Make a Green color Start button
        self._action_button = QPushButton("Start", self)
        self._action_button.setFixedSize(100, 30)
        self._action_button.setStyleSheet("background-color: gray;"
                                          "color: white;"
                                          "font-size: 20px;")

        self._action_button.move(315, 580)
        self._set_action_button_enabled(False)

        self._action_button.clicked.connect(self.__on_action_button_clicked)

    def _render_img_text_label(self):
        self._img_text_label = QLabel("Stopped", self)
        self._img_text_label.setFixedSize(110, 30)
        self._img_text_label.setStyleSheet("background-color: red;"
                                           "color: white;"
                                           "font-size: 20px;")
        self._img_text_label.setAlignment(Qt.AlignCenter)
        self._img_text_label.move(300, 15)

    def _render_game_select_label(self):
        self._game_select_label = QLabel("Select Game", self)
        self._game_select_label.setFixedSize(110, 30)
        self._game_select_label.setStyleSheet("background-color: green;"
                                              "color: white;"
                                              "font-size: 15px;")
        self._game_select_label.setAlignment(Qt.AlignCenter)
        self._game_select_label.move(440, 640)

    def _render_cam_select_label(self):
        self._cam_select_label = QLabel("Select Camera", self)
        self._cam_select_label.setFixedSize(100, 30)
        self._cam_select_label.setStyleSheet("background-color: green;"
                                             "color: white;"
                                             "font-size: 15px;")
        self._cam_select_label.setAlignment(Qt.AlignCenter)
        self._cam_select_label.move(240, 640)

    def _render_menu_bar(self):
        self.options = self.menuBar().addMenu("Options")

        follow_cam = QAction("Follow Cam", self)
        follow_cam.triggered.connect(self._init_connect_cam)
        self.options.addAction(follow_cam)

        gen_adaptor = QAction("Generate", self)
        gen_adaptor.triggered.connect(self._init_no_code_ui)
        self.options.addAction(gen_adaptor)

        select_cam = QAction("Select Cam", self)
        select_cam.triggered.connect(self._init_add_cam)
        self.options.addAction(select_cam)

        # self.follow_cam_menu.addAction(menu_action)

    def _follow_cam_init(self, s):
        print("H")

    def add_cam(self, cam_url: str, cam_name: str):
        print(cam_url)
        new_cam = Camera(cam_url)
        if Camera is None:
            print("Prepared Cam is None")
        self._cam_manger.add_camera(new_cam)
        self._select_cam_combobox.addItem(cam_name)

    def _create_default_camera_manager(self):
        self._cam_manger = CameraManager()
        default_cam = Camera(0)

        self._cam_manger.add_camera(default_cam)
        self._select_cam_combobox.addItem("Default")

    def __on_action_button_clicked(self):
        if self._action_button.text() == "Start":
            self._start_action()
        elif self._action_button.text() == "Stop":
            self._stop_action()

    def _start_action(self):
        self._select_game_combobox.setEnabled(False)
        self._select_cam_combobox.setEnabled(False)

        def action():
            self._action_button.setText("Starting")
            self._action_button.setStyleSheet("background-color: orange;"
                                              "color: white;"
                                              "font-size: 20px;")
            self._voice_assistant.say("Starting in 5 seconds")

            for i in range(5, 0, -1):
                self._voice_assistant.say(str(i))

            self._action_button.setText("Stop")
            self._action_button.setStyleSheet("background-color: red;"
                                              "color: white;"
                                              "font-size: 20px;")

            self._started = True
            self._voice_assistant.say("Started!")

        action_thread = threading.Thread(target=action, daemon=True)
        action_thread.start()

    def _stop_action(self):
        self._started = False

        self._select_game_combobox.setEnabled(True)
        self._select_cam_combobox.setEnabled(True)

        self._action_button.setText("Start")
        self._action_button.setStyleSheet("background-color: green;"
                                          "color: white;"
                                          "font-size: 20px;")
        self._voice_assistant.say("Stopped", True)

    def _on_select_cam_activated(self, index):
        self._cam_manger.select_camera(index)
        if index == 0:
            self._set_action_button_enabled(False)
            self._reset_img_label()

        elif self._select_game_combobox.currentIndex() != 0:
            self._set_action_button_enabled(True)

    def _on_select_game_activated(self, index):
        if index != 0 and self._select_cam_combobox.currentIndex() != 0:
            self._set_action_button_enabled(True)
            self._game_adaptor = self._game_adapters.get(self._select_game_combobox.currentText())
            if self._game_controller is None:
                self._game_controller = GameController(self._game_adaptor())
            else:
                self._game_controller.change_adaptor(self._game_adaptor())

        elif index != 0:
            self._game_adaptor = self._game_adapters.get(self._select_game_combobox.currentText())

            if self._game_controller is None:
                self._game_controller = GameController(self._game_adaptor())
            else:
                self._game_controller.change_adaptor(self._game_adaptor())

        else:
            self._set_action_button_enabled(False)

    def _set_action_button_enabled(self, enabled: bool):
        if enabled:
            self._action_button.setStyleSheet("background-color: green;"
                                              "color: white;"
                                              "font-size: 20px;")
            self._action_button.setEnabled(True)
        else:
            self._action_button.setStyleSheet("background-color: gray;"
                                              "color: white;"
                                              "font-size: 20px;")
            self._action_button.setEnabled(False)

    def _start_process_loop(self):
        def process():

            while True:
                rgb_frame = self._cam_manger.get_current_rgb_frame()  # cv2.Mat object
                if rgb_frame is None:
                    continue

                rgb_frame, landmarks, movement_direction = self.action_tracker.process(rgb_frame)

                self._update_img_label(rgb_frame)

                if movement_direction != "static":
                    # pass
                    self.serial_communicator.send(movement_direction+"\n")

                if not self._started:
                    continue

                action_status = self.action_classifier.classify(landmarks)
                self._game_controller.control_game(action_status)

        process_thread = threading.Thread(target=process, daemon=True)
        process_thread.start()

    def _set_bg(self):
        # Load the PNG image using QPixmap
        pixmap = QPixmap("../assets/bg.png")

        # Set the background of the main window
        self.setFixedSize(pixmap.width(), pixmap.height())
        self.setPixmap(pixmap)

        # Set the background color of the main window to transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def _start_bg_loop(self):
        self._bg_image_label = QLabel(self)
        self.setFixedSize(700, 720)
        # self.move(0, 0)
        self.cap = cv2.VideoCapture("../assets/bg.mp4")
        # self.setAttribute(Qt.WA_Tr)

        def update_label():
            while True:
                ret, frame = self.cap.read()
                if ret:
                    # Convert the cv2 Mat object to a QImage
                    height, width, channel = frame.shape
                    bytes_per_line = 3 * width
                    q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

                    # Scale the QImage to fit the label size
                    scaled_img = q_img.scaled(self._bg_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    # Set the scaled QImage as the image for the label
                    self._bg_image_label.setPixmap(QPixmap.fromImage(scaled_img))


                else:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                time.sleep(.1)

        threading.Thread(target=update_label, daemon=True).start()

    def _reset_img_label(self):
        time.sleep(0.1)
        self._image_label.clear()
        self._image_label.setAlignment(Qt.AlignCenter)
        self._image_label.setText("No Camera Selected")
        self._image_label.setAutoFillBackground(False)

    def _update_img_label(self, frame):
        # Convert the cv2 Mat object to a QImage
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Scale the QImage to fit the label size
        scaled_img = q_img.scaled(self._image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Set the scaled QImage as the image for the label
        self._image_label.setPixmap(QPixmap.fromImage(scaled_img))

    def _init_no_code_ui(self):
        ui = NoCodeUi.NoCodeUi(self)
        threading.Thread(target=ui.show, daemon=True).start()

    def _init_connect_cam(self):
        ui = ConnectCamFollower.ConnectCamFollower(self)
        threading.Thread(target=ui.show, daemon=True).start()

    def _init_add_cam(self):
        ui = AddCamWindow.AddCamWindow(self)
        threading.Thread(target=ui.show, daemon=True).start()