from typing import Callable, Optional, Union

from controllers.fence_step import FenceStep
from controllers.pawn_step import PawnStep
from controllers.utils import PlayerActionKey

from models.player import Player

from view.board import Board
from view.utils import ColorEnum, ColorType


class Person(Player):
    def __init__(self, name: str = 'Player', color: ColorType = ColorEnum.RED):
        super().__init__(name, color)

    def play(
        self,
        board: Board,
        get_valid_pawn_steps: Callable,
        get_valid_fences_step_for_position: Callable,
    ) -> Optional[Union[PawnStep, FenceStep]]:
        while True:
            key = board.get_keyboard()
            if key == PlayerActionKey.PAWN_STEP.value:
                print(self.pawn.position)
                print(get_valid_pawn_steps)
                valid_pawn_steps = get_valid_pawn_steps(self.pawn.position)
                print(valid_pawn_steps)
                with board.draw_valid_pawn_step(self.color, self.name, valid_pawn_steps):
                    click = board.get_mouse()
                    pawn_step = board.get_pawn_step_from_mouse_position(
                        self.pawn, click.x, click.y, valid_pawn_steps
                    )
                if pawn_step is not None:
                    return pawn_step
            if key == PlayerActionKey.FENCE_STEP.value and self.can_fences_step:
                valid_fence_step = get_valid_fences_step_for_position
                click = board.get_mouse()
                fence_step = board.get_fence_step_from_mouse_position(
                    click.x, click.y
                )
                if fence_step is not None:
                    return fence_step
            return None

