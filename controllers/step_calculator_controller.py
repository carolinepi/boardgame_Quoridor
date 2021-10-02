from typing import List, Tuple

from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from view.utils import FenceDirection


class StepCalculatorController:

    def __init__(self, n: int):
        self.n = n
        self.first_n = 0
        self.last_n = self.n - 1
        self.middle_n = int(self.last_n / 2)

    def get_valid_fence_steps_for_position(
            self, position: GridPosition
    ) -> List[FenceStep]:
        column, row = position.column, position.row
        result = []
        if column != self.last_n and row != self.first_n:
            result.append(
                FenceStep(position, FenceDirection.HORIZONTAL)
            )
        if column != self.first_n and row != self.last_n:
            result.append(
                FenceStep(position, FenceDirection.VERTICAL)
            )
        return result

    def get_valid_pawn_steps(
            self,
            position: GridPosition,
            players_positions: List[GridPosition],
            blocked_moves: List[Tuple[int]]
    ) -> List[PawnStep]:
        column, row = position.column, position.row
        result = []
        blocked_coordinates = self.get_blocked_coordinates_for_position(position, blocked_moves)
        if column != self.first_n and (column - 1, row) not in blocked_coordinates:
            if (column - 1, row) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(position.left(), blocked_moves)

                if column - 1 != self.first_n and (column - 2, row) not in blocked:
                    result.append(PawnStep(position, position.left().left()))
                else:
                    if column - 1 != self.first_n and row != self.last_n \
                            and (column - 1, row + 1) not in blocked + blocked_coordinates:
                        result.append(PawnStep(position, position.left().bottom()))
                    if column - 1 != self.first_n and row != self.first_n \
                            and (column - 1, row + 1) not in blocked + blocked_coordinates:
                        result.append(PawnStep(position, position.left().top()))
            else:
                result.append(PawnStep(position, position.left()))

        if column != self.last_n and (column + 1, row) not in blocked_coordinates:
            if (column + 1, row) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(position.right(), blocked_moves)

                if column + 1 != self.last_n and (column + 2, row) not in blocked:
                    result.append(PawnStep(position, position.right().right()))
                else:
                    if column + 1 != self.last_n and row != self.last_n \
                            and (column + 1, row + 1) not in blocked + blocked_coordinates:
                        result.append(PawnStep(position, position.right().bottom()))
                    if column + 1 != self.last_n and row != self.first_n \
                            and (column + 1, row - 1) not in blocked + blocked_coordinates:
                        result.append(PawnStep(position, position.right().bottom()))
            else:
                result.append(PawnStep(position, position.right()))
        if row != self.first_n:
            if (column, row - 1) in players_positions and (column, row - 1) not in blocked_coordinates:
                blocked = self.get_blocked_coordinates_for_position(position.top(), blocked_moves)

                if row - 1 != self.first_n and (column, row - 2) not in blocked:
                    result.append(PawnStep(position, position.top().top()))
                else:
                    if row - 1 != self.first_n and column + 1 != self.last_n \
                            and (column+1, row-1) not in blocked+blocked_coordinates:
                        result.append(PawnStep(position, position.top().right()))
                    if row - 1 != self.first_n and column - 1 != self.first_n \
                            and (column-1, row-1) not in blocked+blocked_coordinates:
                        result.append(PawnStep(position, position.top().left()))
            else:
                result.append(PawnStep(position, position.top()))
        if row != self.last_n and (column, row + 1) not in blocked_coordinates:
            if (column, row + 1) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(position.bottom(), blocked_moves)

                if row + 1 != self.last_n and (column, row + 2) not in blocked:
                    result.append(PawnStep(position, position.bottom().bottom()))
                else:
                    if row + 1 != self.last_n and column + 1 != self.last_n \
                            and (column + 1, row + 1) not in blocked + blocked_coordinates:
                        result.append(PawnStep(position, position.bottom().right()))
                    if row + 1 != self.last_n and column - 1 != self.first_n \
                            and (column - 1, row + 1) not in blocked + blocked_coordinates:
                        result.append(PawnStep(position, position.bottom().left()))
            else:
                result.append(PawnStep(position, position.bottom()))
        return result

    def get_blocked_coordinates_for_position(self, position, blocked_moves):
        blocked_coordinates = []
        for move in blocked_moves:
            if position == move[0]:
                blocked_coordinates.append((move[1].column, move[1].row))
            elif position == move[1]:
                blocked_coordinates.append((move[0].column, move[0].row))

        return blocked_coordinates
