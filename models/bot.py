import random
from typing import Optional, Union, List

from exception import NoWayError
from models.fence_step import FenceStep
from models.pawn_step import PawnStep
from models.player import Player

from view.board import Board


class Bot(Player):

    @staticmethod
    def random_pawn_move(valid_pawn_steps: List[PawnStep]):
        try:
            return random.choice(valid_pawn_steps)
        except IndexError:
            raise NoWayError

    @staticmethod
    def random_put_fence(valid_fence_steps: List[FenceStep]):
        try:
            return random.choice(valid_fence_steps)
        except IndexError:
            raise NoWayError

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
