from contextlib import contextmanager
from typing import List, Optional

from graphics import GraphWin, Point

from controllers.config_controller import Config
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from view.facade import PawnFigure, Background
from view.fence import Fence

from view.field import Field
from view.pawn import Pawn
from view.utils import ColorEnum, FenceDirection


class Board:

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
        self.middle_n = int(self.last_n / 2)
        self.first_n = 0
        self.window = None

    def create_window(self) -> None:
        side = self.square_size * self.n + self.inner_size * (self.n - 1)
        self.window = GraphWin("Quoridor", side, side)

    def draw(self) -> None:
        background = Background(
            Point(0, 0),
            Point(self.n, self.n),
            ColorEnum.WHITE
        )
        background.draw(self.window)
        for column in range(self.n):
            for row in range(self.n):
                field = self.field[column][row].get_field_figure()
                field.draw(self.window)

    def draw_pawn(self, pawn: Pawn, field: Field) -> PawnFigure:
        figure = pawn.get_figure(field, self.square_size)
        figure.draw(self.window)
        return figure

    def undraw_pawn(self, pawn: Pawn) -> None:
        pawn.current_element.undraw()

    def draw_fence(self, fence: Fence, field: Field) -> None:
        rectangle = fence.get_figure(
            field, self.square_size, self.inner_size
        )
        rectangle.draw(self.window)

    def undraw_fence(self, fence: Fence):
        fence.current_element.undraw()

    def get_field(self, position: GridPosition) -> Field:
        return self.field[position.column][position.row]

    def close_window(self) -> None:
        self.window.close()

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

    def get_keyboard(self) -> str:
        return self.window.getKey()

    def get_mouse(self) -> Point:
        return self.window.getMouse()

    @contextmanager
    def draw_valid_pawn_step(
        self,
        name: str,
        valid_steps: List[PawnStep]
    ):
        hiding_elements = []
        for valid_step in valid_steps:
            position = valid_step.to_position.clone()
            possible_pawn = Pawn(
                position=position,
                color=ColorEnum.BLACK,
                name=name
            )
            field = self.get_field(position)
            hiding_elements.append(self.draw_pawn(possible_pawn, field))
        yield
        for hiding_element in hiding_elements:
            hiding_element.undraw()

    def get_field_from_mouse_position(self, x: int, y: int) -> Optional[Field]:
        if x % self.size > self.square_size or y % self.size > self.square_size:
            return None
        return self.field[int(x / self.size)][int(y / self.size)]

    def get_pawn_step_from_mouse_position(
        self, pawn: Pawn, x: int, y: int, valid_pawn_steps: List[PawnStep]
    ) -> Optional[PawnStep]:
        field = self.get_field_from_mouse_position(x, y)
        if field is None:
            return None

        is_valid = False
        for valid_pawn_step in valid_pawn_steps:
            if valid_pawn_step.to_position == field.position:
                is_valid = True
                continue
        if field is not None and is_valid:
            return PawnStep(pawn.position, field.position)
        return None
    
    def get_fence_step_from_mouse_position(
        self, x: int, y: int,
    ) -> Optional[FenceStep]:
        if self.get_field_from_mouse_position(x, y) is not None:
            return None
        # vertical fence
        if x % self.size > self.square_size and y % self.size < self.square_size:
            field = self.get_field_from_mouse_position(x + self.square_size, y)
            return FenceStep(field.position, FenceDirection.VERTICAL)
            # return FenceStep(field.position, FenceDirection.VERTICAL) if self.isValidFencePlacing(field.position, FenceDirection.VERTICAL) else None
        # horizontal fence
        if x % self.size < self.square_size and y % self.size > self.square_size:
            field = self.get_field_from_mouse_position(x, y + self.square_size)
            # return FenceStep(field.position, FenceDirection.HORIZONTAL) if self.isValidFencePlacing(field.position, FenceDirection.HORIZONTAL) else None
            return FenceStep(field.position, FenceDirection.HORIZONTAL)
        # on inner crossing space
        if x % self.size > self.square_size and y % self.size > self.square_size:
            field = self.get_field_from_mouse_position(x + self.square_size, y + self.square_size)
            direction = FenceDirection.HORIZONTAL if field.left - x < field.top - y else FenceDirection.VERTICAL
            # return FenceStep(field.position, direction) if self.isValidFencePlacing(field.position, direction) else None
            return FenceStep(field.position, direction)
        return None

    def move_pawn(self, pawn: Pawn, field: Field) -> None:
        self.undraw_pawn(pawn)
        self.draw_pawn(pawn, field)

    def put_fence(self, fence: Fence, field: Field) -> None:
        self.draw_fence(fence, field)
