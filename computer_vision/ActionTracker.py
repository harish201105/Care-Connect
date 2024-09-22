import time

import cv2
import mediapipe as mp


class ActionTracker:
    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self._mp_pose = mp.solutions.pose
        self._pose = self._mp_pose.Pose(static_image_mode=static_image_mode, model_complexity=model_complexity,
                                        smooth_landmarks=smooth_landmarks,
                                        min_detection_confidence=min_detection_confidence,
                                        min_tracking_confidence=min_tracking_confidence)

        self._previous_body_pos = None
        self._body_move_threshold = 5
        self._previous_body_move_time = None
        self._body_move_time_threshold = 0.5
        self._expection_occured = False

    def __del__(self):
        self._pose.close()

    def process(self, img: cv2.Mat):
        # Process the image and get the pose landmarks
        results = self._pose.process(img)
        landmarks = self._find_most_likely_pos(results.pose_landmarks)

        movement_direction = "static"

        # Draw the landmarks on the image
        if landmarks is not None:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(img, landmarks, self._mp_pose.POSE_CONNECTIONS)

            movement_direction = self._track_body(landmarks)

        return img, landmarks, movement_direction

    def _track_body(self, landmarks):
        if self._previous_body_pos is None:
            self._previous_body_pos = self._find_center_point(landmarks.landmark[self._mp_pose.PoseLandmark.RIGHT_SHOULDER],
                                                              landmarks.landmark[self._mp_pose.PoseLandmark.LEFT_SHOULDER])
            return "static"

        current_body_pos = self._find_center_point(landmarks.landmark[self._mp_pose.PoseLandmark.RIGHT_SHOULDER],
                                                   landmarks.landmark[self._mp_pose.PoseLandmark.LEFT_SHOULDER])

        # Calculate the difference between the current and previous body positions
        diff_x = current_body_pos - self._previous_body_pos

        # Determine if the body has moved left, right, or is static
        if abs(diff_x) > self._body_move_threshold:
            if diff_x > 0:
                direction = "left"
            else:
                direction = "right"
        else:
            direction = "static"

        if self._previous_body_move_time is None:
            self._previous_body_move_time = time.time()

        current_time = time.time()
        if current_time - self._previous_body_move_time > self._body_move_time_threshold:
            self._previous_body_pos = current_body_pos
            self._previous_body_move_time = current_time

        return direction

    @staticmethod
    def _find_center_point(right_shoulder, left_shoulder):
        return ((right_shoulder.x + left_shoulder.x)/2)*100

    def _find_most_likely_pos(self, landmarks):
        try:
            if not self._expection_occured:
                # Initialize variables to keep track of the most confident landmark and its confidence score
                most_confident_landmark = None
                max_confidence = 0

                # Iterate through all the landmarks
                for landmark in landmarks.landmark:
                    # Check if the landmark has a confidence score and if it's higher than the current max
                    if landmark.HasField('visibility') and landmark.visibility > max_confidence:
                        max_confidence = landmark.visibility
                        most_confident_landmark = landmark

                # If a confident landmark was found, return a new PoseLandmark object with just that landmark
                if most_confident_landmark is not None:
                    new_landmarks = self._mp_pose.PoseLandmark()
                    new_landmarks.CopyFrom(most_confident_landmark)
                    return new_landmarks

        except Exception as e:
            self._expection_occured = True
        return landmarks
            