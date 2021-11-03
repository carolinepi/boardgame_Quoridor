import random
from copy import copy, deepcopy
from typing import List, Tuple

from controllers.step_calculator_controller import StepCalculatorController
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from models.player import Player
from view.fence import Fence


class AiCalculator:

    def __init__(
        self,
        n: int,
        calculator_controller: StepCalculatorController,
        another_player: Player,
    ):
        self.max_depth = 3
        self.fences_to_change_depth = 15
        self.factors = [0.75, 0.15, 0.05, 0.05]
        self.calculator_controller = calculator_controller
        self.previous_row = float('inf')
        self.previous_column = float('inf')
        self.n = n
        self.first_n = 0
        self.last_n = self.n - 1
        self.another_player = deepcopy(another_player)

    def choose_step(self, player1: Player):
        new_player1 = deepcopy(player1)
        if len(
            new_player1.fences + self.another_player.fences
        ) == self.fences_to_change_depth:
            self.max_depth += 1
            self.fences_to_change_depth -= 5

        alpha_beta = -1
        step = None
        possible_moves_fence, possible_moves_player_1, _ = \
            self.get_valid_steps_for_player(new_player1, self.another_player)
        # for possible_move in possible_moves_player_1:
        #     new_player1.pawn.set_position(
        #         GridPosition(
        #             possible_move.to_position.row,
        #             possible_move.to_position.column
        #         )
        #     )
        check = False

        if (
            len(possible_moves_player_1) > 1 and
            self.previous_row != float('inf')
        ):
            check = True

        for possible_move in possible_moves_player_1:
            if (
                check and
                possible_move.to_position.row == self.previous_row and
                possible_move.to_position.column == self.previous_column
            ):
                continue
            new_player1.pawn.set_position(
                GridPosition(
                    possible_move.to_position.row,
                    possible_move.to_position.column
                )
            )
            result = self.minimax_tree(
                1, new_player1, self.another_player, self.first_n, self.last_n
            )

            if (
                result > alpha_beta or
                (result == alpha_beta and random.randint(0, 10) < 5)
            ):
                alpha_beta = result
                step = possible_move

        if new_player1.can_fences_step:
            for possible_move_fence in possible_moves_fence:
                new_player1.put_fence(
                    possible_move_fence.position, possible_move_fence.direction
                )
                result = self.minimax_tree(
                    1, new_player1, self.another_player, self.first_n, self.last_n
                )
                if result > alpha_beta or (
                    result == alpha_beta
                    and random.randint(0, 10) < 5
                    and not isinstance(step, PawnStep)
                ):
                    alpha_beta = result

        if isinstance(step, PawnStep):
            self.previous_row = new_player1.pawn.position.row
            self.previous_column = new_player1.pawn.position.column
        else:
            self.previous_row = float('inf')
            self.previous_column = float('inf')
        return step

    @property
    def max_heuristic(self):
        return 45 * self.factors[0] + 10 * self.factors[1] \
               + 20 * self.factors[2] + 5 * self.factors[3]

    def get_alpha_beta_from_end_position(
        self, new_player1: Player, player2: Player
    ):
        if new_player1.pawn.position.row == self.last_n:
            return self.last_n
        if player2.pawn.position.row == self.first_n:
            return self.first_n
        return None

    def minimax_tree(
        self, depth: int, new_player1: Player, player2: Player, l: int, r: int
    ):
        if depth == self.max_depth:
            return self.get_heuristic(new_player1, player2)

        alpha_beta_from_end_position = self.get_alpha_beta_from_end_position(
            new_player1, player2
        )
        if alpha_beta_from_end_position:
            return alpha_beta_from_end_position

        possible_moves_fence, possible_moves_player_1, possible_moves_player_2 = \
            self.get_valid_steps_for_player(new_player1, player2)
        print(f'possible_moves_player_1 {possible_moves_player_1}')
        print(f'possible_moves_player_2 {possible_moves_player_2}')

        if depth % 2 == 1:
            alpha_beta = self.last_n

            for possible_move in possible_moves_player_2:
                player2.pawn.set_position(
                    GridPosition(
                        possible_move.to_position.row,
                        possible_move.to_position.column
                    )
                )
                result = self.minimax_tree(depth + 1, new_player1, player2, l, r)
                alpha_beta = min(alpha_beta, result)
                if result <= l:
                    return alpha_beta

            if player2.can_fences_step:
                for possible_move_fence in possible_moves_fence:
                    player2.put_fence(
                        possible_move_fence.position,
                        possible_move_fence.direction
                    )
                    result = self.minimax_tree(
                        depth + 1, new_player1, player2, self.first_n, self.last_n
                    )
                    alpha_beta = min(alpha_beta, result)
                    if result >= r:
                        return alpha_beta
        else:
            alpha_beta = self.first_n

            for possible_move in possible_moves_player_1:
                new_player1.pawn.set_position(
                    GridPosition(
                        possible_move.to_position.row,
                        possible_move.to_position.column
                    )
                )
                result = self.minimax_tree(depth + 1, new_player1, player2, l, r)
                alpha_beta = max(alpha_beta, result)
                if result >= r:
                    return alpha_beta

            if new_player1.can_fences_step:
                for possible_move_fence in possible_moves_fence:
                    new_player1.put_fence(
                        possible_move_fence.position,
                        possible_move_fence.direction
                    )
                    result = self.minimax_tree(
                        depth + 1, new_player1, player2, self.first_n, self.last_n
                    )
                    alpha_beta = max(alpha_beta, result)
                    if result >= r:
                        return alpha_beta
        return alpha_beta

    def get_heuristic(self, new_player1: Player, player2: Player):
        _, possible_moves_player_1, possible_moves_player_2 = \
            self.get_valid_steps_for_player(new_player1, player2)

        alpha_beta_from_end_position = self.get_alpha_beta_from_end_position(
            new_player1, player2
        )
        if alpha_beta_from_end_position:
            return alpha_beta_from_end_position

        factors = []
        # factors[0] = self.factors[0] * (short_path_depth_player2 - shortest_path_depth_player1)
        factors.append(self.factors[1] * (
            len(new_player1.fences) - len(player2.fences)
        ))
        factors.append(self.factors[3] * (
            len(possible_moves_player_1) - len(possible_moves_player_2)
        ) + self.max_heuristic)

        return sum(factors) / (2 * self.max_heuristic)

    @staticmethod
    def get_fences_blocked_moves(
        fences: List[Fence]
    ) -> List[Tuple[GridPosition, GridPosition]]:
        moves = []
        for fence in fences:
            moves.extend(fence.coordinates)

        return moves

    @staticmethod
    def get_all_fences(new_player1: Player, player2: Player) -> List[Fence]:
        fences = []
        fences.extend(new_player1.fences)
        fences.extend(player2.fences)

        return fences

    @staticmethod
    def get_players_current_and_start_positions(
        new_player1: Player, player2: Player
    ) -> List[Tuple[GridPosition, GridPosition]]:
        return [
            (new_player1.pawn.position, new_player1.start_position),
            (player2.pawn.position, player2.start_position)
        ]

    def get_valid_steps_for_player(
        self, new_player1: Player, player2: Player
    ) -> Tuple[List[FenceStep], List[PawnStep], List[PawnStep]]:
        fences = self.get_all_fences(new_player1, player2)
        blocked_moves = self.get_fences_blocked_moves(fences)
        players_current_and_start_positions = \
            self.get_players_current_and_start_positions(new_player1, player2)
        valid_fence_steps = self.calculator_controller.get_valid_fence_steps(
            fences,
            blocked_moves,
            players_current_and_start_positions
        )
        valid_pawn_steps_for_player1 = self.calculator_controller. \
            get_valid_pawn_steps(
                new_player1.pawn.position,
                [(player2.pawn.position.column, player2.pawn.position.row)],
                blocked_moves
            )
        valid_pawn_steps_for_player2 = self.calculator_controller. \
            get_valid_pawn_steps(
                player2.pawn.position,
                [(new_player1.pawn.position.column, new_player1.pawn.position.row)],
                blocked_moves
            )
        return (
            valid_fence_steps,
            valid_pawn_steps_for_player1,
            valid_pawn_steps_for_player2,
        )
