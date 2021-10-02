from typing import List

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

    def get_valid_pawn_steps_for_position(
        self, position: GridPosition
    ) -> List[PawnStep]:
        column, row = position.column, position.row
        result = []
        if column != self.first_n:
            if column == self.first_n + 1 and row == self.middle_n:  # left pawn
                result.append(
                    PawnStep(position, position.left().top(), position.left())
                )
                result.append(
                    PawnStep(position, position.left().bottom(), position.left())
                )
            elif column == self.middle_n + 1 and (row == self.first_n or row == self.last_n):  # top and bottom pawns
                result.append(
                    PawnStep(position, position.left().left(), position.left())
                )
            else:
                result.append(PawnStep(position, position.left()))
        if column != self.last_n:
            if column == self.last_n - 1 and row == self.middle_n:  # right pawn
                result.append(
                    PawnStep(position, position.right().top(), position.right())
                )
                result.append(
                    PawnStep(position, position.right().bottom(), position.right())
                )
            elif column == self.middle_n - 1 and (row == self.first_n or row == self.last_n):  # top and bottom pawns
                result.append(
                    PawnStep(position, position.right().right(), position.right())
                )
            else:
                result.append(PawnStep(position, position.right()))
        if row != self.first_n:
            if column == self.middle_n and row == self.first_n + 1:  # top pawn
                result.append(
                    PawnStep(position, position.top().left(), position.top())
                )
                result.append(
                    PawnStep(position, position.top().right(), position.top())
                )
            elif (column == self.first_n or column == self.last_n) and row == self.middle_n + 1:  # left and right pawns
                result.append(
                    PawnStep(position, position.top().top(), position.top())
                )
            else:
                result.append(PawnStep(position, position.top()))
        if row != self.last_n:
            if column == self.middle_n and row == self.last_n - 1:  # bottom pawn
                result.append(
                    PawnStep(position, position.bottom().left(), position.bottom())
                )
                result.append(
                    PawnStep(position, position.bottom().right(), position.bottom())
                )
            elif (column == self.first_n or column == self.last_n) and row == self.middle_n - 1:  # left and right pawns
                result.append(
                    PawnStep(position, position.bottom().bottom(), position.bottom())
                )
            else:
                result.append(PawnStep(position, position.bottom()))
        return result

    def get_valid_pawn_steps_ignoring_for_position(
        self, position: GridPosition
    ) -> List[PawnStep]:
        column, row = position.column, position.row
        result = []
        if column != self.first_n:
            result.append(PawnStep(position, position.left()))
        if column != self.last_n:
            result.append(PawnStep(position, position.right()))
        if row != self.first_n:
            result.append(PawnStep(position, position.top()))
        if row != self.last_n:
            result.append(PawnStep(position, position.bottom()))
        return result

    # def get_valid_steps(self):
    #     for column in range(self.n):
    #         for row in range(self.n):
    #             position = GridPosition(column, row)
    #             self.valid_fences_step.extend(
    #                 self.get_valid_fence_steps_for_position(position)
    #             )
    #             self.valid_pawns_step[position] = \
    #                 self.get_valid_pawn_steps_for_position(position)
    #             self.valid_pawns_step_ignore_other[position] = \
    #                 self.get_valid_pawn_steps_ignoring_for_position(position)

    def get_intersection_valid_pawn_steps_for_position(
        self, position: GridPosition
    ) -> List[PawnStep]:
        return list(
            set(self.get_valid_pawn_steps_for_position(position))
            &
            set(self.get_valid_pawn_steps_ignoring_for_position(position))
        )
