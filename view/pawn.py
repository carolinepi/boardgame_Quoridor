from typing import Tuple, Optional

from graphics import Text, Circle

from grid_position import GridPosition
from view.field import Field
from view.utils import Color


class Pawn:
    def __init__(
        self,
        position: GridPosition,
        color: Color,
        name: str,
    ):
        self.position = position
        self.color = color
        self.name = name

    def get_circle_and_label(
        self, field: Field, fill_color: Optional[Color], square_size: int
    ) -> Tuple[Circle, Text]:
        center = field.middle_point
        radius = int(square_size * 0.4)
        circle = Circle(center, radius)
        circle.setFill(self.color.value if fill_color is None else fill_color)
        circle.setWidth(0)
        label = Text(center, self.name[:1])
        label.setSize(min(max(5, int(square_size / 2)), 36))
        label.setStyle("bold")
        label.setTextColor(Color.WHITE.value)
        return circle, label
