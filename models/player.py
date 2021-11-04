from copy import deepcopy
from typing import List, Union, Optional

from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep

from view.board import Board
from view.fence import Fence
from view.field import Field
from view.pawn import Pawn
from view.utils import ColorEnum, FenceDirection


class Player:
    LIMIT_FENCES = 10

    def __init__(self, name: str = 'Player', color: ColorEnum = ColorEnum.RED):
        self.name = name
        self.color = color
        self.pawn = None
        self.fences = []
        self.start_position = None
        self.end_position = []
        self.score = 0

    def set_start_position(self, position: GridPosition):
        self.start_position = position

    def set_end_position(self, positions: List[GridPosition]):
        self.end_position = positions

    def set_pawn(self):
        self.pawn = Pawn(self.start_position, self.color, self.name)

    def play(
        self,
        board: Board,
        valid_pawn_steps: List[PawnStep],
        valid_fence_steps: List[FenceStep],
    ) -> Optional[Union[PawnStep, FenceStep]]:
        pass

    def move_pawn(self, field: Field) -> None:
        self.pawn.position = field.position
        print(f'{self.name} moved to {field.position}')

    def move_pawn_to_position(self, position: GridPosition) -> None:
        self.pawn.position = position
        print(f'{self.name} moved to {position}')

    def put_fence(
        self, position: GridPosition, direction: FenceDirection
    ) -> Fence:
        fence = Fence(position, self.color, direction)
        self.fences.append(fence)
        print(f'{self.name} put fence to {position}')
        return fence

    @property
    def can_fences_step(self):
        if len(self.fences) >= self.LIMIT_FENCES:
            print(f'{self.name} can`t put fence. Limit: {self.LIMIT_FENCES}')
            return False
        return True

    @property
    def has_won(self) -> bool:
        return self.pawn.position in self.end_position

    def clean_player_data(self) -> None:
        self.pawn = None
        self.fences = []
        self.start_position = None
        self.end_position = []

    def inc_score(self) -> int:
        self.score += 1
        return self.score

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name} ({self.color})'

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
