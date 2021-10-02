from models.grid_position import GridPosition
from view.utils import FenceDirection


class FenceStep:
    def __init__(self, position: GridPosition, direction: FenceDirection):
        self.position = position
        self.direction = direction
