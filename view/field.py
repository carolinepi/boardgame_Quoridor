from graphics import Rectangle, Point

from grid_position import GridPosition
from view.utils import Color


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

    def get_rectangle(self, color=Color.SQUARE.value) -> Rectangle:
        top_left = Point(self.left, self.top)
        bottom_right = Point(self.right, self.bottom)
        rectangle = Rectangle(top_left, bottom_right)
        rectangle.setFill(color)
        rectangle.setWidth(0)
        return rectangle

    @property
    def middle_point(self) -> Point:
        middle_square_size = int(self.square_size / 2)
        return Point(
            self.left + middle_square_size,
            self.top + middle_square_size
        )
