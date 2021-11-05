from copy import deepcopy

from models.grid_position import GridPosition
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

    @property
    def current_element(self):
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
