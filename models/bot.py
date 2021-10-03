import random
from typing import Optional, Union, List

from models.fence_step import FenceStep
from models.pawn_step import PawnStep

from models.player import Player

from view.board import Board
from view.utils import ColorEnum


class Bot(Player):
    def __init__(self, name: str = 'Player', color: ColorEnum = ColorEnum.RED):
        super().__init__(name, color)

    @staticmethod
    def random_pawn_move(valid_pawn_steps: List[PawnStep]):
        return random.choice(valid_pawn_steps)

    @staticmethod
    def random_put_fence(valid_fence_steps: List[FenceStep]):
        return random.choice(valid_fence_steps)

    def play(
        self,
        board: Board,
        valid_pawn_steps: List[PawnStep],
        valid_fence_steps: List[FenceStep],
    ) -> Optional[Union[PawnStep, FenceStep]]:
        pawn_move = self.random_pawn_move(valid_pawn_steps)
        put_fence = self.random_put_fence(valid_fence_steps)
        return random.choice([put_fence, pawn_move])

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name} ({self.color})'
