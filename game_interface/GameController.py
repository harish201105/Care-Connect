from game_interface import GameAdaptor
from computer_vision import ActionStatus


class GameController:
    def __init__(self, game_adaptor: GameAdaptor):
        self._game_adaptor = game_adaptor

    def change_adaptor(self, game_adaptor: GameAdaptor):
        self._game_adaptor = game_adaptor

    def control_game(self, action_status: ActionStatus):
        if action_status is None:
            self._game_adaptor.on_no_action()
            return

        if action_status.leg_movement is not None:
            self._game_adaptor.on_leg_movement(action_status.leg_movement)

        if action_status.head_movement is not None:
            self._game_adaptor.on_head_movement(action_status.head_movement)

        if action_status.arm_movement is not None:
            self._game_adaptor.on_arm_movement(action_status.arm_movement)

        if action_status.head_pose is not None:
            self._game_adaptor.on_head_tilt(action_status.head_pose)
