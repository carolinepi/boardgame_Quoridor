from typing import Tuple

from graphics import Text, Circle

from controllers.grid_position import GridPosition
from view.field import Field
from view.utils import ColorEnum, ColorType


class Pawn:
    def __init__(
        self,
        position: GridPosition,
        color: ColorType,
        name: str,
    ):
        self.position = position
        self.color = color
        self.name = name
        self.current_elements = []

    def get_circle_and_label(
        self, field: Field, square_size: int
    ) -> Tuple[Circle, Text]:
        center = field.middle_point
        radius = int(square_size * 0.4)
        circle = Circle(center, radius)
        circle.setFill(self.color.value)
        circle.setWidth(0)
        label = Text(center, self.name[:1])
        label.setSize(min(max(5, int(square_size / 2)), 36))
        label.setStyle("bold")
        label.setTextColor(ColorEnum.WHITE.value)
        self.current_elements = [circle, label]
        return circle, label

    def move(self, field: Field, square_size: int):
        self.position = field.position
        return self.get_circle_and_label(field, square_size)

