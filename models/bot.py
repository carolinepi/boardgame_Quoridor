import random
from typing import Optional, Union, List

from models.fence_step import FenceStep
from models.pawn_step import PawnStep

from models.player import Player

from view.board import Board
from view.utils import ColorEnum, ColorType


class Bot(Player):
    def __init__(self, name: str = 'Player', color: ColorType = ColorEnum.RED):
        super().__init__(name, color)

    @staticmethod
    def random_pawn_move(valid_pawn_steps: List[PawnStep]):
        return random.choice(valid_pawn_steps)

    def play(
        self,
        board: Board,
        valid_pawn_steps: List[PawnStep],
        valid_fence_steps: List[FenceStep],
    ) -> Optional[Union[PawnStep, FenceStep]]:
        return self.random_pawn_move(valid_pawn_steps)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name} ({self.color})'
