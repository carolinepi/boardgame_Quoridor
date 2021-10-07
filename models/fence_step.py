from models.grid_position import GridPosition
from view.utils import FenceDirection


class FenceStep:
    def __init__(self, position: GridPosition, direction: FenceDirection):
        self.position = position
        self.direction = direction

    def __repr__(self):
        return f'FenceStep({self.position.column}, {self.position.row}, ' \
               f'{self.direction})'

    def __eq__(self, other: 'FenceStep'):
        return (
            self.position == other.position and
            self.direction == other.direction
        )

    def __hash__(self):
        return hash((self.position, self.direction))
