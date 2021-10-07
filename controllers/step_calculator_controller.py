from typing import List, Tuple, Any

from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from view.utils import FenceDirection


class StepCalculatorController:

    def __init__(self, n: int):
        self.n = n
        self.first_n = 0
        self.last_n = self.n - 1
        self.middle_n = self.last_n // 2

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
            players_positions:  List[Tuple[Any, Any]],
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
        if row != self.first_n and (column, row - 1) not in blocked_coordinates:
            if (column, row - 1) in players_positions:
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

    def get_valid_fence_steps(self, fences, blocked_moves):
        valid_fence_steps = []
        fences_position = [(fence.position, fence.direction) for fence in fences]
        fences_position.extend(self.get_blocked_grids_for_fences(fences))

        print(fences_position)

        for row in range(self.last_n):
            for column in range(1, self.last_n+1):

                position = GridPosition(column, row)
                if (position, FenceDirection.HORIZONTAL) not in fences_position:
                    valid_fence_steps.append(FenceStep(position, FenceDirection.HORIZONTAL))

                if (position, FenceDirection.VERTICAL) not in fences_position:
                    valid_fence_steps.append(FenceStep(position, FenceDirection.VERTICAL))

        return valid_fence_steps

    def get_blocked_grids_for_fences(self, fences):
        positions = []
        for fence in fences:
            if fence.direction == FenceDirection.VERTICAL:
                positions.append((fence.position.bottom(), FenceDirection.VERTICAL))
                positions.append((fence.position.bottom().left(), FenceDirection.HORIZONTAL))
            else:
                positions.append((fence.position.right(), FenceDirection.HORIZONTAL))
                positions.append((fence.position.right().top(), FenceDirection.VERTICAL))

        return positions
