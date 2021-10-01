from typing import Callable, List, Union, Optional

from controllers.fence_step import FenceStep
from controllers.grid_position import GridPosition
from controllers.pawn_step import PawnStep

from view.board import Board
from view.field import Field
from view.pawn import Pawn
from view.utils import ColorEnum, ColorType


class Player:
    LIMIT_FENCES = 10

    def __init__(self, name: str = 'Player', color: ColorType = ColorEnum.RED):
        self.name = name
        self.color = color
        self.pawn = None
        self.fences = []
        self.start_position = None
        self.end_position = []

    def set_start_position(self, position: GridPosition):
        self.start_position = position

    def set_end_position(self, positions: List[GridPosition]):
        self.end_position = positions

    def set_pawn(self):
        self.pawn = Pawn(self.start_position, self.color, self.name)

    def play(
        self,
        board: Board,
        get_valid_pawn_steps: Callable,
        get_valid_fences_step_for_position: Callable,
    ) -> Optional[Union[PawnStep, FenceStep]]:
        pass

    def move_pawn(self, field: Field) -> None:
        self.pawn.position = field.position
        print(f'{self.name} moved to {field.position}')

    @property
    def can_fences_step(self):
        return len(self.fences) < self.LIMIT_FENCES

    @property
    def has_won(self) -> bool:
        return True if self.pawn.position in self.end_position else False

    def __str__(self) -> str:
        return "%s (%s)" % (self.name, self.color.name)


