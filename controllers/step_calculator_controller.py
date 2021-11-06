from typing import List, Tuple, Dict

from controllers.dijkstra import calculate_path_from_position, calculate_shortest_path_from_position
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from view.fence import Fence
from view.utils import FenceDirection, ColorEnum


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
        players_positions: List[Tuple[int, int]],
        blocked_moves: List[Tuple[GridPosition, GridPosition]]
    ) -> List[PawnStep]:
        column, row = position.column, position.row
        result = []
        blocked_coordinates = self.get_blocked_coordinates_for_position(
            position=position,
            blocked_moves=blocked_moves
        )

        if column != self.first_n and \
           (column - 1, row) not in blocked_coordinates:
            if (column - 1, row) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(
                    position=position.left(),
                    blocked_moves=blocked_moves
                )

                if column - 1 != self.first_n and \
                   (column - 2, row) not in blocked:
                    result.append(PawnStep(position, position.left().left()))
                elif column - 1 != self.first_n:
                    blocked += blocked_coordinates
                    if column != self.first_n and \
                       row != self.last_n and \
                       (column - 1, row + 1) not in blocked:
                        result.append(PawnStep(position, position.left().bottom()))
                    if column != self.first_n and \
                       row != self.first_n and \
                       (column - 1, row - 1) not in blocked:
                        result.append(PawnStep(position, position.left().top()))
            else:
                result.append(PawnStep(position, position.left()))

        if column != self.last_n and \
           (column + 1, row) not in blocked_coordinates:
            if (column + 1, row) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(
                    position=position.right(),
                    blocked_moves=blocked_moves
                )

                if column + 1 != self.last_n and \
                   (column + 2, row) not in blocked:
                    result.append(PawnStep(position, position.right().right()))
                elif column + 1 != self.last_n:
                    blocked += blocked_coordinates
                    if column != self.last_n and \
                       row != self.last_n and \
                       (column + 1, row + 1) not in blocked:
                        result.append(
                            PawnStep(position, position.right().top())
                        )
                    if column != self.last_n and \
                       row != self.first_n and \
                       (column + 1, row - 1) not in blocked:
                        result.append(
                            PawnStep(position, position.right().bottom())
                        )
            else:
                result.append(PawnStep(position, position.right()))

        if row != self.first_n and (column, row - 1) not in blocked_coordinates:
            if (column, row - 1) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(
                    position=position.top(),
                    blocked_moves=blocked_moves)

                if row - 1 != self.first_n and (column, row - 2) not in blocked:
                    result.append(PawnStep(position, position.top().top()))
                elif row - 1 != self.first_n:
                    blocked += blocked_coordinates
                    if row != self.first_n and \
                       column != self.last_n and \
                       (column + 1, row - 1) not in blocked:
                        result.append(
                            PawnStep(position, position.top().right())
                        )
                    if row != self.first_n and \
                       column != self.first_n and \
                       (column - 1, row - 1) not in blocked:
                        result.append(
                            PawnStep(position, position.top().left())
                        )
            else:
                result.append(PawnStep(position, position.top()))

        if row != self.last_n and (column, row + 1) not in blocked_coordinates:
            if (column, row + 1) in players_positions:
                blocked = self.get_blocked_coordinates_for_position(
                    position=position.bottom(),
                    blocked_moves=blocked_moves)

                if row + 1 != self.last_n and (column, row + 2) not in blocked:
                    result.append(
                        PawnStep(position, position.bottom().bottom())
                    )
                elif row + 1 != self.last_n:
                    blocked += blocked_coordinates
                    if row != self.last_n and \
                       column != self.last_n and \
                       (column + 1, row + 1) not in blocked:
                        result.append(
                            PawnStep(position, position.bottom().right())
                        )
                    if row != self.last_n and \
                       column != self.first_n and \
                       (column - 1, row + 1) not in blocked:
                        result.append(
                            PawnStep(position, position.bottom().left())
                        )
            else:
                result.append(PawnStep(position, position.bottom()))
        return result

    @staticmethod
    def get_blocked_coordinates_for_position(
        position: GridPosition,
        blocked_moves: List[Tuple[GridPosition, GridPosition]]
    ) -> List[Tuple[int, int]]:
        blocked_coordinates = []
        for move in blocked_moves:
            if position == move[0]:
                blocked_coordinates.append((move[1].column, move[1].row))
            elif position == move[1]:
                blocked_coordinates.append((move[0].column, move[0].row))

        return blocked_coordinates

    def get_valid_fence_steps(
        self,
        fences: List[Fence],
        blocked_moves: List[Tuple[GridPosition, GridPosition]],
        players_positions: List[Tuple[GridPosition, GridPosition]]
    ) -> List[FenceStep]:
        valid_fence_steps = []
        fences_position = [
            (fence.position, fence.direction) for fence in fences
        ]
        fences_position.extend(self.get_blocked_grids_for_fences(fences))

        for row in range(self.n):
            for column in range(0, self.n):

                position = GridPosition(column, row)
                if row != 0 and column != self.last_n and \
                   (position, FenceDirection.HORIZONTAL) not in fences_position:
                    step_is_valid = self._check_new_fence_valid(
                        position=position,
                        direction=FenceDirection.HORIZONTAL,
                        blocked_moves=blocked_moves,
                        players_position=players_positions
                    )

                    if step_is_valid:
                        valid_fence_steps.append(
                            FenceStep(position, FenceDirection.HORIZONTAL)
                        )

                if row != self.last_n and column != self.first_n and \
                   (position, FenceDirection.VERTICAL) not in fences_position:
                    step_is_valid = self._check_new_fence_valid(
                        position=position,
                        direction=FenceDirection.VERTICAL,
                        blocked_moves=blocked_moves,
                        players_position=players_positions
                    )

                    if step_is_valid:
                        valid_fence_steps.append(
                            FenceStep(position, FenceDirection.VERTICAL)
                        )

        return valid_fence_steps

    def _check_new_fence_valid(
        self,
        position: GridPosition,
        direction: FenceDirection,
        blocked_moves: List[Tuple[GridPosition, GridPosition]],
        players_position: List[Tuple[GridPosition, GridPosition]]
    ) -> bool:
        fence = Fence(position, ColorEnum.RED, direction)
        new_blocked_moves = blocked_moves + fence.coordinates
        valid_step = False

        for player_position in players_position:
            valid_step = self.is_fence_step_valid(
                player_position[0],
                new_blocked_moves,
                player_position[1])
            if not valid_step:
                break

        return valid_step

    @staticmethod
    def get_blocked_grids_for_fences(
        fences: List[Fence]
    ) -> List[Tuple[GridPosition, FenceDirection]]:
        positions = []
        for fence in fences:
            if fence.direction == FenceDirection.VERTICAL:
                positions.append(
                    (fence.position.bottom(), FenceDirection.VERTICAL)
                )
                positions.append(
                    (fence.position.top(), FenceDirection.VERTICAL)
                )
                positions.append(
                    (fence.position.bottom().left(), FenceDirection.HORIZONTAL)
                )
            else:
                positions.append(
                    (fence.position.left(), FenceDirection.HORIZONTAL)
                )
                positions.append(
                    (fence.position.right(), FenceDirection.HORIZONTAL)
                )
                positions.append(
                    (fence.position.right().top(), FenceDirection.VERTICAL)
                )

        return positions

    def is_fence_step_valid(
        self,
        position: GridPosition,
        blocked_moves: List[Tuple[GridPosition, GridPosition]],
        player_start_position: GridPosition
    ) -> bool:
        matrix = self._get_moves_to_grid(blocked_moves)
        last_row = self.last_n

        if player_start_position.row == self.last_n:
            last_row = self.first_n

        for column in range(self.n):
            result = calculate_path_from_position(
                matrix=matrix,
                position=position,
                destination=GridPosition(column, last_row)
            )

            if result:
                return result

        return False

    def _get_moves_to_grid(
        self,
        blocked_moves: List[Tuple[GridPosition, GridPosition]]
    ) -> Dict[GridPosition, Dict[GridPosition, int]]:
        moves = {}
        for row in range(self.n):
            for column in range(self.n):
                grid = GridPosition(column, row)
                blocked_coordinates = self.get_blocked_coordinates_for_position(
                    position=grid,
                    blocked_moves=blocked_moves
                )
                result = {}
                if column != self.first_n and \
                   (column - 1, row) not in blocked_coordinates:
                    result[GridPosition(column - 1, row)] = 1
                if column != self.last_n and \
                   (column + 1, row) not in blocked_coordinates:
                    result[GridPosition(column + 1, row)] = 1
                if row != self.first_n and \
                   (column, row - 1) not in blocked_coordinates:
                    result[GridPosition(column, row - 1)] = 1
                if row != self.last_n and \
                   (column, row + 1) not in blocked_coordinates:
                    result[GridPosition(column, row + 1)] = 1

                moves[grid] = result

        return moves

    def get_shortest_path_from_position(
        self,
        position: GridPosition,
        blocked_moves: List[Tuple[GridPosition, GridPosition]],
        last_positions: List[GridPosition]
    ) -> int:
        last_grids = {}
        # path = []

        matrix = self._get_moves_to_grid(blocked_moves)
        previous_grids, visited = calculate_shortest_path_from_position(
            matrix=matrix,
            position=position
        )

        for grid in last_positions:
            last_grids[grid] = visited[grid]

        destination = min(last_grids, key=last_grids.get)

        # grid = destination
        # while grid != position:
        #     path.append(grid)
        #     if grid in previous_grids:
        #         grid = previous_grids[grid]
        #     else:
        #         path = []
        #         break
        #
        # if path:
        #     path.append(position)
        #     path.reverse()

        # return path, last_grids[destination]
        return last_grids[destination]

    @staticmethod
    def get_valid_fences_around_position(
            position: GridPosition,
            available_fences: List[FenceStep]
    ) -> List[FenceStep]:
        blocked_for_position = {
            FenceStep(position, FenceDirection.VERTICAL),
            FenceStep(position, FenceDirection.HORIZONTAL),
            FenceStep(position.right(), FenceDirection.VERTICAL),
            FenceStep(position.top(), FenceDirection.VERTICAL),
            FenceStep(position.top().right(), FenceDirection.VERTICAL),
            FenceStep(position.left(), FenceDirection.HORIZONTAL),
            FenceStep(position.bottom(), FenceDirection.HORIZONTAL),
            FenceStep(position.bottom().left(), FenceDirection.HORIZONTAL),
        }

        return list(set(available_fences).intersection(blocked_for_position))

    @staticmethod
    def get_fences_blocked_moves(
        fences: List[Fence]
    ) -> List[Tuple[GridPosition, GridPosition]]:
        steps = []
        for fence in fences:
            steps.extend(fence.coordinates)

        return steps
