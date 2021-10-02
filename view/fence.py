from graphics import Rectangle, Point

from models.grid_position import GridPosition
from view.field import Field
from view.utils import FenceDirection, ColorType


class Fence:
    def __init__(
        self,
        position: GridPosition,
        color: ColorType,
        direction: FenceDirection
    ):
        self.position = position
        self.direction = direction
        self.color = color

    def get_rectangle(
        self,
        field: Field,
        square_size: int,
        inner_size: int,
    ) -> Rectangle:
        height = 2 * square_size + inner_size
        width = inner_size
        rectangle = None
        if self.direction == FenceDirection.HORIZONTAL:
            rectangle = Rectangle(
                Point(field.left, field.top - width),
                Point(field.left + height, field.top)
            )
        if self.direction == FenceDirection.VERTICAL:
            rectangle = Rectangle(
                Point(field.left - width, field.top),
                Point(field.left, field.top + height)
            )
        rectangle.setFill(self.color.value)
        rectangle.setWidth(0)
        return rectangle
