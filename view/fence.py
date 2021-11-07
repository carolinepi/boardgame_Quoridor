from copy import deepcopy


from models.grid_position import GridPosition
from view.utils import FenceDirection, ColorEnum


class Fence:
    def __init__(
        self,
        position: GridPosition,
        color: ColorEnum,
        direction: FenceDirection,
    ):
        self.position = position
        self.direction = direction
        self.color = color
        self.coordinates = [[self.position, ], ]
        self._current_element = None
        self._figure = None

        if self.direction == FenceDirection.HORIZONTAL:
            self.coordinates.append(
                [self.position.right(), self.position.right().top()]
            )
            self.coordinates[0].append(self.position.top())
        if self.direction == FenceDirection.VERTICAL:
            self.coordinates.append(
                [self.position.bottom(), self.position.bottom().left()]
            )
            self.coordinates[0].append(self.position.left())

    def __deepcopy__(self, memo) -> 'Fence':
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        result.position = deepcopy(self.position, memo)
        result.coordinates = deepcopy(self.coordinates, memo)
        result.color = deepcopy(self.color, memo)
        result.direction = deepcopy(self.direction, memo)
        return result
