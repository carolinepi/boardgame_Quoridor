import random
from typing import Callable, Optional, Union

from controllers.fence_step import FenceStep
from controllers.pawn_step import PawnStep

from models.player import Player

from view.board import Board
from view.utils import ColorEnum, ColorType


class Bot(Player):
    def __init__(self, name: str = 'Player', color: ColorType = ColorEnum.RED):
        super().__init__(name, color)

    def random_move(self, get_valid_pawn_steps: Callable):
        valid_pawn_steps = get_valid_pawn_steps(self.pawn.position)
        return random.choice(valid_pawn_steps)

    def play(
        self,
        board: Board,
        get_valid_pawn_steps: Callable,
        get_valid_fences_step_for_position: Callable,
    ) -> Optional[Union[PawnStep, FenceStep]]:
        return self.random_move(get_valid_pawn_steps)
