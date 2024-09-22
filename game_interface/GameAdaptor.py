from abc import ABCMeta, abstractmethod

from computer_vision import LegMovement, HeadMovement, HeadPose, ArmMovement

import pyautogui as input_controller


class GameAdaptor(metaclass=ABCMeta):
    def __init__(self):
        self._input_controller = input_controller
        self._input_controller.FAILSAFE = False

        self._RUNNING_GAP_THRESHOLD = 0.85

        self._already_running = False
        self._already_squat = False
        self._already_straight = False

        self._already_right_tilt = False
        self._already_left_tilt = False

        self._already_right_arm_raised = False
        self._already_right_arm_bended = False

        self._last_run_time = None
        self._last_jump_time = None

    @classmethod
    @abstractmethod
    def on_leg_movement(cls, leg_movement: LegMovement):
        pass

    @classmethod
    @abstractmethod
    def on_head_movement(cls, head_movement: HeadMovement):
        pass

    @classmethod
    @abstractmethod
    def on_arm_movement(cls, arm_movement: ArmMovement):
        pass

    @classmethod
    @abstractmethod
    def on_head_tilt(cls, head_pose: HeadPose):
        pass

    @classmethod
    @abstractmethod
    def on_no_action(cls):
        pass
