from typing import List

from grid_position import GridPosition
from view.pawn import Pawn
from view.utils import Color

LIMIT_FENCES = 10


class Player:
    def __init__(self, name: str = 'Player', color: Color = None):
        self.name = name
        self.color = color
        self.pawn = None
        self.fences = []
        self.score = 0
        self.startPosition = None
        self.endPositions = []

    def set_start_position(self, position: GridPosition):
        self.startPosition = position

    def set_end_position(self, positions: List[GridPosition]):
        self.endPositions = positions

    def set_pawn(self):
        self.pawn = Pawn(self.startPosition, self.color, self.name)

    def play(self):
        pass

    # def move_pawn(self, position: GridPosition):
    #     print("player %s moved his pawn to %s" % (self.name, position))
    #     self.pawn.move(position)

    @property
    def fences_len(self):
        return len(self.fences)

    def has_won(self) -> bool:
        for endPosition in self.endPositions:
            return True if self.pawn.coord == endPosition else False

    def __str__(self) -> str:
        return "%s (%s)" % (self.name, self.color.name)


