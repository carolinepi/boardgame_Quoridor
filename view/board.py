from typing import List, Optional

from graphics import GraphWin, Rectangle, Point

from grid_position import GridPosition
from view.field import Field
from view.pawn import Pawn
from view.utils import Color


class Board:
    n = 9
    square_size = 32
    inner_size = 4
    totalFenceCount = 20
    window = None

    def __init__(self):
        self.field = [
            [
                Field(
                    GridPosition(column, row), self.square_size, self.inner_size
                )
                for row in range(self.n)
            ]
            for column in range(self.n)
        ]

    def create_window(self) -> None:
        side = self.square_size * self.n + self.inner_size * (self.n - 1)
        self.window = GraphWin("Quoridor", side, side)

    def draw(self) -> None:
        background = Rectangle(Point(0, 0), Point(self.n, self.n))
        background.setFill(Color.WHITE.value)
        background.setWidth(0)
        background.draw(self.window)
        for column in range(self.n):
            for row in range(self.n):
                rectangle = self.field[column][row].get_rectangle()
                rectangle.draw(self.window)

    def draw_pawn(
        self, pawn: Pawn, field: Field, fill_color: Optional[Color] = None
    ) -> None:
        circle, label = pawn.get_circle_and_label(
            field, fill_color, self.square_size
        )
        circle.draw(self.window)
        label.draw(self.window)

    def get_field(self, position: GridPosition) -> Field:
        return self.field[position.column][position.row]

    def close_window(self) -> None:
        self.window.close()

    def get_start_positions(self) -> List[GridPosition]:
        middle_n = int((self.n - 1) / 2)
        first_n = 0
        last_n = self.n - 1
        return [
            GridPosition(middle_n, first_n),
            GridPosition(middle_n, last_n)
        ]

    def get_end_positions(
        self, start_position: GridPosition
    ) -> List[GridPosition]:
        first_n = 0
        last_n = self.n - 1
        if start_position.column == first_n:
            return [GridPosition(i, last_n) for i in range(self.n)]
        if start_position.column == last_n:
            return [GridPosition(i, first_n) for i in range(self.n)]
        return []
