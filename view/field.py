from models.grid_position import GridPosition
from view.utils import ColorEnum


class Field:
    def __init__(
        self,
        position: GridPosition,
        square_size: int,
        inner_size: int
    ):
        self.position = position
        self.square_size = square_size
        self.inner_size = inner_size
        size = self.square_size + self.inner_size
        self.left = size * self.position.column
        self.right = self.left + self.square_size
        self.top = size * self.position.row
        self.bottom = self.top + self.square_size

