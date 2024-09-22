import threading

import cv2


class Camera:
    def __init__(self, cam_id):
        self._cam_id = cam_id
        self._video_stream = None
        self._currentframe = None
        self._reading = None

    def __del__(self):
        self.stop_reading()
        self.disconnect()

    def connect(self) -> bool:
        self._video_stream = cv2.VideoCapture(self._cam_id)
        return self._video_stream.isOpened()

    def disconnect(self):
        if self._video_stream:
            self._video_stream.release()
            self._video_stream = None

    def start_reading(self):
        self._reading = True

        def process():
            while self._reading and self._video_stream is not None:
                ret, frame = self._video_stream.read()
                if ret:
                    self._currentframe = frame

        process_thread = threading.Thread(target=process)
        process_thread.daemon = True
        process_thread.start()

    def stop_reading(self):
        self._reading = False

    def get_currentframe(self):
        if self._currentframe is not None and self._reading:
            return cv2.resize(self._currentframe, (500, 500))

        return None
