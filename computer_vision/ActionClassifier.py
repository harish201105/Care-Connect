import math

from mediapipe.python.solutions.pose import PoseLandmark

from computer_vision import ActionStatus, HeadPose, HeadMovement, Direction, LegMovement, ArmMovement


class ActionClassifier:
    def __init__(self):
        self._HEAD_TILT_THRESHOLD_ANGLE = 10
        self._HEAD_MOVEMENT_THRESHOLD = 2
        self._LEG_BEND_THRESHOLD_ANGLE = 173
        self._ARM_BEND_THRESHOLD_ANGLE = 45
        self._JUMP_THRESHOLD = 80

        self._PREVIOUS_MOUTH_POS = None

        self._previous_head_position = None

    def classify(self, landmarks) -> ActionStatus:
        if landmarks is None:
            return None

        result = ActionStatus()
        result.head_pose = self._classify_head_pose(landmarks)
        result.head_movement = self._classify_head_movement(landmarks)
        result.leg_movement = self._classify_leg_movement(landmarks)
        result.arm_movement = self._classify_arm_movement(landmarks)

        return result

    def _classify_head_pose(self, landmarks) -> HeadPose:
        left_eye_outer = landmarks.landmark[PoseLandmark.LEFT_EYE_OUTER]
        right_eye_outer = landmarks.landmark[PoseLandmark.RIGHT_EYE_OUTER]

        eye_line_slope = ActionClassifier.__calc_angle(left_eye_outer, right_eye_outer)

        if eye_line_slope > self._HEAD_TILT_THRESHOLD_ANGLE:
            return HeadPose.Left_Tilted
        elif eye_line_slope < -self._HEAD_TILT_THRESHOLD_ANGLE:
            return HeadPose.Right_Tilted
        else:
            return HeadPose.Straight

    def _classify_head_movement(self, landmarks) -> HeadMovement:
        head_landmarks = [PoseLandmark.NOSE, PoseLandmark.LEFT_EYE_INNER, PoseLandmark.LEFT_EYE,
                          PoseLandmark.LEFT_EYE_OUTER, PoseLandmark.RIGHT_EYE_INNER, PoseLandmark.RIGHT_EYE,
                          PoseLandmark.RIGHT_EYE_OUTER, PoseLandmark.LEFT_EAR, PoseLandmark.RIGHT_EAR,
                          PoseLandmark.MOUTH_LEFT, PoseLandmark.MOUTH_RIGHT]

        num_landmarks = len(head_landmarks)
        sum_y = sum([landmarks.landmark[i].y for i in head_landmarks])
        avg_y = sum_y / num_landmarks

        current_head_position = avg_y

        if self._previous_head_position is None:
            self._previous_head_position = current_head_position

        distance_moved = (self._previous_head_position - current_head_position) * 1000

        head_movement = HeadMovement()
        head_movement.direction = Direction.Static
        head_movement.distance = 0

        if abs(distance_moved) > self._HEAD_MOVEMENT_THRESHOLD:
            head_movement.distance = distance_moved
            if distance_moved > 0:
                head_movement.direction = Direction.Up
            else:
                head_movement.direction = Direction.Down

        self._previous_head_position = current_head_position

        return head_movement

    def _classify_leg_movement(self, landmarks) -> LegMovement:
        if self._PREVIOUS_MOUTH_POS is None:
            self._PREVIOUS_MOUTH_POS = landmarks.landmark[PoseLandmark.MOUTH_LEFT]
        elif self._PREVIOUS_MOUTH_POS.y > landmarks.landmark[PoseLandmark.LEFT_SHOULDER].y:
            return LegMovement.Jump

        left_hip = landmarks.landmark[PoseLandmark.LEFT_HIP]
        left_knee = landmarks.landmark[PoseLandmark.LEFT_KNEE]
        left_ankle = landmarks.landmark[PoseLandmark.LEFT_ANKLE]

        left_leg_angle = self.__calc_angle(left_hip, left_knee, left_ankle)

        right_hip = landmarks.landmark[PoseLandmark.RIGHT_HIP]
        right_knee = landmarks.landmark[PoseLandmark.RIGHT_KNEE]
        right_ankle = landmarks.landmark[PoseLandmark.RIGHT_ANKLE]

        right_leg_angle = self.__calc_angle(right_hip, right_knee, right_ankle)

        right_leg_bended = True if right_leg_angle < self._LEG_BEND_THRESHOLD_ANGLE else False
        left_leg_bended = True if left_leg_angle < self._LEG_BEND_THRESHOLD_ANGLE else False

        if right_leg_bended and left_leg_bended:
            return LegMovement.Squat
        elif (not right_leg_bended) and (not left_leg_bended):
            return LegMovement.Straight
        else:
            self.__previous_leg_position = [right_leg_bended, left_leg_bended]
            return LegMovement.Running

    def _classify_arm_movement(self, landmarks) -> ArmMovement:
        right_shoulder = landmarks.landmark[PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks.landmark[PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks.landmark[PoseLandmark.RIGHT_WRIST]

        left_shoulder = landmarks.landmark[PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks.landmark[PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks.landmark[PoseLandmark.LEFT_WRIST]

        right_arm_angle = self.__calc_angle(right_shoulder, right_elbow, right_wrist)
        left_arm_angle = self.__calc_angle(left_shoulder, left_elbow, left_wrist)

        arm_movement = ArmMovement()

        arm_movement.RIGHT_ARM_RAISED = right_shoulder.y > right_wrist.y
        arm_movement.LEFT_ARM_RAISED = left_shoulder.y > left_wrist.y
        arm_movement.RIGHT_ARM_BENDED = right_arm_angle < self._ARM_BEND_THRESHOLD_ANGLE
        arm_movement.LEFT_ARM_BENDED = left_arm_angle < self._ARM_BEND_THRESHOLD_ANGLE

        return arm_movement

    @staticmethod
    def __calc_angle(point_1, point_2, point_3=None):
        if point_3 is None:
            if point_1.x == point_2.x:
                return float('inf')
            else:
                slope = (point_2.y - point_1.y) / (point_2.x - point_1.x)
                return math.degrees(math.atan(slope))
        else:
            # calculate angle between three points
            x1, y1 = point_1.x, point_1.y
            x2, y2 = point_2.x, point_2.y
            x3, y3 = point_3.x, point_3.y

            # Calculate vectors between points
            v1 = (x1 - x2, y1 - y2)
            v2 = (x3 - x2, y3 - y2)

            # Calculate dot product and magnitudes
            dot_product = v1[0] * v2[0] + v1[1] * v2[1]
            mag_v1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
            mag_v2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

            # Calculate angle in degrees
            angle_radians = math.acos(dot_product / (mag_v1 * mag_v2))
            angle_degrees = math.degrees(angle_radians)

            return angle_degrees
