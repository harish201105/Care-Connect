from enum import Enum


class Direction(Enum):
    Left: bytes = 0
    Right: bytes = 1
    Up: bytes = 2
    Down: bytes = 3
    Static: bytes = 4


class HeadPose(Enum):
    Right_Tilted: bytes = 0
    Left_Tilted:  bytes = 1
    Straight: bytes = 2


class HeadMovement:
    direction: Direction
    distance: int


class LegMovement(Enum):
    Running: bytes = 0
    Jump: bytes = 1
    Squat: bytes = 2
    Straight: bytes = 3


class ArmMovement:
    LEFT_ARM_BENDED: bool
    RIGHT_ARM_BENDED: bool
    LEFT_ARM_RAISED: bool
    RIGHT_ARM_RAISED: bool


class ActionStatus:
    head_pose: HeadPose
    head_movement: HeadMovement
    leg_movement: LegMovement
    arm_movement: ArmMovement
