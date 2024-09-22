import sys

from PyQt5.QtWidgets import QFileDialog, QLabel, QLineEdit, QPushButton, QGridLayout, \
    QDoubleSpinBox, QApplication, QDialog
from pathlib import Path


class NoCodeUi(QDialog):
    def __init__(self, parent_window):
        super().__init__(parent_window)
        # self.setFixedSize(300, 550)
        self.initUi()  # Load the user interface
        self.setStyleSheet("background-color: #E2D1F9;")

        self.input_file_button.clicked.connect(self.get_input_file) # connect the input file button to get_input_file method
        self.output_file_button.clicked.connect(self.get_output_file) # connect the output file button to get_output_file method
        self.generate_button.clicked.connect(self.generate_code) # connect the submit button to the generate_code method

    def initUi(self):
        # Set window title and size
        self.setWindowTitle("Adaptor Generator")

        # Create widgets
        self.input_file_label = QLabel("Select Template:")
        self.input_file_edit = QLineEdit()
        self.input_file_button = QPushButton("Select Template")
        self.output_file_label = QLabel("Output path:")
        self.output_file_edit = QLineEdit()
        self.output_file_button = QPushButton("Output path")
        self.adaptor_name_label = QLabel("Adaptor Name:")
        self.adaptor_name_edit = QLineEdit()
        self.run_key_label = QLabel("Run Key:")
        self.run_key_edit = QLineEdit()
        self.cam_left_key_label = QLabel("Cam Left Key:")
        self.cam_left_key_edit = QLineEdit()
        self.cam_right_key_label = QLabel("Cam Right Key:")
        self.cam_right_key_edit = QLineEdit()
        self.weapon_swing_key_label = QLabel("Weapon Swing Key:")
        self.weapon_swing_key_edit = QLineEdit()
        self.jump_key_label = QLabel("Jump Key:")
        self.jump_key_edit = QLineEdit()
        self.running_gap_threshold_label = QLabel("Running Gap Threshold:")
        self.running_gap_threshold_spinbox = QDoubleSpinBox()
        self.running_gap_threshold_spinbox.setRange(0.0, 1.0)
        self.running_gap_threshold_spinbox.setSingleStep(0.01)
        self.running_gap_threshold_spinbox.setValue(0.85)
        self.generate_button = QPushButton("Generate")

        # Create layout and add widgets
        layout = QGridLayout()
        layout.addWidget(self.input_file_label, 0, 0)
        layout.addWidget(self.input_file_edit, 0, 1)
        layout.addWidget(self.input_file_button, 0, 2)
        layout.addWidget(self.output_file_label, 1, 0)
        layout.addWidget(self.output_file_edit, 1, 1)
        layout.addWidget(self.output_file_button, 1, 2)
        layout.addWidget(self.adaptor_name_label, 2, 0)
        layout.addWidget(self.adaptor_name_edit, 2, 1)
        layout.addWidget(self.run_key_label, 3, 0)
        layout.addWidget(self.run_key_edit, 3, 1)
        layout.addWidget(self.cam_left_key_label, 4, 0)
        layout.addWidget(self.cam_left_key_edit, 4, 1)
        layout.addWidget(self.cam_right_key_label, 5, 0)
        layout.addWidget(self.cam_right_key_edit, 5, 1)
        layout.addWidget(self.weapon_swing_key_label, 6, 0)
        layout.addWidget(self.weapon_swing_key_edit, 6, 1)
        layout.addWidget(self.jump_key_label, 7, 0)
        layout.addWidget(self.jump_key_edit, 7, 1)
        layout.addWidget(self.running_gap_threshold_label, 8, 0)
        layout.addWidget(self.running_gap_threshold_spinbox, 8, 1)
        layout.addWidget(self.generate_button, 9, 1)

        # Set layout
        self.setLayout(layout)
        self.show()

    def get_input_file(self):
        file_dialog = QFileDialog()
        self.input_file_edit.setText(file_dialog.getOpenFileName(self, 'Open File', str(Path.home()), '*.template')[0])

    def get_output_file(self):
        file_dialog = QFileDialog()
        self.output_file_edit.setText(file_dialog.getSaveFileName(self, 'Save File', str(Path.home()), '*.py')[0])

    def generate_code(self):
        # Read the input file
        input_file_path = self.input_file_edit.text()
        with open(input_file_path, 'r') as f:
            file_content = f.read()

        # Get the values from the user
        adaptor_name = self.adaptor_name_edit.text()
        run_key = self.run_key_edit.text()
        cam_left_key = self.cam_left_key_edit.text()
        cam_right_key = self.cam_right_key_edit.text()
        weapon_swing_key = self.weapon_swing_key_edit.text()
        jump_key = self.jump_key_edit.text()
        running_gap_threshold = self.running_gap_threshold_spinbox.text()

        # Replace the placeholders in the file content
        file_content = file_content.replace('{.AdaptorName.}', adaptor_name)
        file_content = file_content.replace('{.RUN_KEY.}', run_key)
        file_content = file_content.replace('{.CAM_LEFT_KEY.}', cam_left_key)
        file_content = file_content.replace('{.CAM_RIGHT_KEY.}', cam_right_key)
        file_content = file_content.replace('{.WEAPON_SWING_KEY.}', weapon_swing_key)
        file_content = file_content.replace('{.JUMP_KEY.}', jump_key)
        file_content = file_content.replace('{._RUNNING_GAP_THRESHOLD.}', running_gap_threshold)

        # Write the generated code to the output file
        output_file_path = self.output_file_edit.text()
        with open(output_file_path, 'w') as f:
            f.write(file_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoCodeUi()
    window.show()
    sys.exit(app.exec_())
