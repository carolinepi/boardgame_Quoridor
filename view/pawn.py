from models.grid_position import GridPosition
from view.facade import PawnFigure
from view.field import Field
from view.utils import ColorType


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
        self._figure = None

    def get_figure(self, field: Field, square_size: int) -> PawnFigure:
        center = field.middle_point
        radius = int(square_size * 0.4)
        label_size = (min(max(5, int(square_size / 2)), 36))
        self._figure = PawnFigure(
            center, radius, self.name[:1], self.color, label_size
        )
        return self._figure

    def move(self, field: Field, square_size: int):
        self.position = field.position
        return self.get_figure(field, square_size)

    @property
    def current_element(self) -> PawnFigure:
        if self._figure is not None:
            return self._figure

