from typing import Optional

from models.grid_position import GridPosition


class PawnStep:
    def __init__(
        self,
        from_position: GridPosition,
        to_position: GridPosition,
        through_position: Optional[GridPosition] = None
    ):
        self.from_position = from_position
        self.to_position = to_position
        self.through_position = through_position

    @property
    def is_jump(self):
        return self.through_position is not None

    def __str__(self):
        return f'PawnStep({self.to_position.column}, {self.to_position.row})'

    def __repr__(self):
        return f'PawnStep({self.to_position.column}, {self.to_position.row})'

    def __eq__(self, other: 'PawnStep'):
        return (
            self.from_position == other.from_position and
            self.to_position == other.to_position
        )

    def __ne__(self, other: 'PawnStep'):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_position, self.to_position))
