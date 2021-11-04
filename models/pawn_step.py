from typing import Optional

from models.grid_position import GridPosition
from view.utils import StepType


class PawnStep:
    def __init__(
        self,
        from_position: GridPosition,
        to_position: GridPosition,
        through_position: Optional[GridPosition] = None,
        step_type: Optional[StepType] = StepType.MOVE
    ):
        self.from_position = from_position
        self.to_position = to_position
        self.through_position = through_position
        self.step_type = step_type

    @property
    def is_jump(self):
        return self.through_position is not None

    def __repr__(self):
        return f'PawnStep({self.to_position.column}, {self.to_position.row})'

    def __eq__(self, other: 'PawnStep'):
        return (
            self.from_position == other.from_position and
            self.to_position == other.to_position
        )

    def __hash__(self):
        return hash((self.from_position, self.to_position))
