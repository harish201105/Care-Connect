import cv2

from computer_vision import Camera


class CameraManager:
    def __init__(self):
        self._cameras = []
        self._selected_camera = None

        self._cameras.append(None)

    def add_camera(self, cam: Camera):
        self._cameras.append(cam)

    def remove_camera(self, index: int):
        if self._selected_camera is not None:
            self._selected_camera.stop_reading()
            self._selected_camera.disconnect()

        del self._cameras[index]

    def select_camera(self, index: int):
        if self._selected_camera is not None:
            self._selected_camera.stop_reading()
            self._selected_camera.disconnect()

        self._selected_camera = self._cameras[index]

        if self._selected_camera is not None:
            self._selected_camera.connect()
            self._selected_camera.start_reading()

    def get_current_rgb_frame(self):
        if self._selected_camera is None:
            return None

        frame = self._selected_camera.get_currentframe()

        if frame is None:
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgb_frame
