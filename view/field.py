from graphics import Point

from models.grid_position import GridPosition
from view.facade import FieldFigure
from view.utils import ColorEnum


class Field:
    def __init__(self, position: GridPosition, square_size: int, inner_size: int):
        self.position = position
        self.square_size = square_size
        self.inner_size = inner_size
        size = self.square_size + self.inner_size
        self.left = size * self.position.column
        self.right = self.left + self.square_size
        self.top = size * self.position.row
        self.bottom = self.top + self.square_size

    def get_field_figure(self, color=ColorEnum.SNOW) -> FieldFigure:
        top_left = Point(self.left, self.top)
        bottom_right = Point(self.right, self.bottom)
        return FieldFigure(top_left, bottom_right, color)

    @property
    def middle_point(self) -> Point:
        middle_square_size = int(self.square_size / 2)
        return Point(
            self.left + middle_square_size,
            self.top + middle_square_size
        )
