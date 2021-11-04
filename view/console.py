from contextlib import contextmanager
from typing import List, Optional

from controllers.config_controller import Config
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from view.field import Field
from view.pawn import Pawn
from view.utils import FenceDirection, ColorEnum


class Console:
    def __init__(self, config: Config):
        self.n = config.n
        self.square_size = config.square_size
        self.inner_size = config.inner_size
        self.size = self.square_size + self.inner_size
        self.field = [
            [
                Field(
                    GridPosition(column, row), self.square_size, self.inner_size
                )
                for row in range(self.n)
            ]
            for column in range(self.n)
        ]
        self.last_n = self.n - 1
        self.middle_n = self.last_n // 2
        self.first_n = 0

    def get_field(self, position: GridPosition) -> Field:
        return self.field[position.column][position.row]

    def get_start_positions(self) -> List[GridPosition]:
        return [
            GridPosition(self.middle_n, self.first_n),
            GridPosition(self.middle_n, self.last_n)
        ]

    def get_end_positions(
        self, start_position: GridPosition
    ) -> List[GridPosition]:
        if start_position.row == self.first_n:
            return [GridPosition(i, self.last_n) for i in range(self.n)]
        if start_position.row == self.last_n:
            return [GridPosition(i, self.first_n) for i in range(self.n)]
        return []

    def get_keyboard(self):
        step = input().strip()
        return step.split()

    @staticmethod
    def exit():
        print("finish game")
        exit()
