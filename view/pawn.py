from copy import deepcopy
from typing import Optional

from models.grid_position import GridPosition
from view.facade import PawnFigure
from view.field import Field
from view.utils import ColorEnum


class Pawn:
    def __init__(
        self,
        position: GridPosition,
        color: ColorEnum,
        name: str,
    ):
        self.position = position
        self.color = color
        self.name = name
        self._figure = None

    def set_position(self, position: GridPosition):
        self.position = position

    def get_figure(self, field: Field, square_size: int) -> PawnFigure:
        center = field.middle_point
        radius = int(square_size * 0.4)
        label_size = (min(max(5, int(square_size / 2)), 36))
        self._figure = PawnFigure(
            center, radius, self.name[:1], self.color, label_size
        )
        return self._figure

    @property
    def current_element(self) -> Optional[PawnFigure]:
        if self._figure is not None:
            return self._figure

    def __deepcopy__(self, memo) -> 'Pawn':
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.position = deepcopy(self.position, memo)
        result.color = deepcopy(self.color, memo)
        result.name = deepcopy(self.name, memo)
        return result
