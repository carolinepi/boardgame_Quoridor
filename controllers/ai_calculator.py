import random
from copy import copy, deepcopy
from typing import List, Tuple, Optional

from controllers.step_calculator_controller import StepCalculatorController
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from models.player import Player
from view.fence import Fence


class AiCalculator:

    def __init__(
        self,
        calculator_controller: StepCalculatorController,
        another_player: Player,
    ):
        self.max_depth = 3
        self.factors = [0.75, 0.15, 0.05, 0.05]
        self.calculator_controller = calculator_controller
        self.another_player = deepcopy(another_player)

    def choose_step(self, player: Player):
        new_player1 = deepcopy(player)

        best_value, best_move = self.minimax_tree(
            0, new_player1, self.another_player, float('-inf'), float('inf'), False
        )
        print(f'FINAL: {best_value}')
        return best_move

    @property
    def max_heuristic(self):
        return 45 * self.factors[0] + 10 * self.factors[1] \
               + 20 * self.factors[2] + 5 * self.factors[3]

    # def get_alpha_beta_from_end_position(
    #     self, new_player1: Player, player2: Player
    # ):
    #     if new_player1.pawn.position.row == self.last_n:
    #         return self.last_n
    #     if player2.pawn.position.row == self.first_n:
    #         return self.first_n
    #     return None

    def minimax_tree(
        self,
        depth: int,
        new_player1: Player,
        player2: Player,
        alpha: float,
        beta: float,
        is_max_turn: bool,
        last_fence: Optional[Fence] = None
    ):
        print(f'depth = {depth}, alpha = {alpha}, beta = {beta}, player1 = {new_player1.pawn.position}')
        best_move = None
        if depth == self.max_depth:
            if last_fence:
                new_player1.fences.remove(last_fence)
            print(f'if depth == self.max_depth: {self.get_evaluation_function(new_player1, player2)} {best_move}')
            return self.get_evaluation_function(new_player1, player2), best_move

        possible_moves_fence, possible_moves_player_1, _ = \
            self.get_valid_steps_for_player(new_player1, player2)
        random.shuffle(possible_moves_player_1)
        print(f'possible_moves_player_1 {possible_moves_player_1}')
        best_value = float('-inf') if is_max_turn else float('inf')
        for possible_move in possible_moves_player_1:
            new_player1.pawn.set_position(
                GridPosition(
                    possible_move.to_position.column,
                    possible_move.to_position.row
                )
            )
            child_result, child_move = self.minimax_tree(
                depth + 1, new_player1, player2, alpha, beta, not is_max_turn
            )
            print(f'is_max_turn = {is_max_turn} best_value = {best_value}, child_result = {child_result}')
            if is_max_turn and best_value < child_result:
                best_value = child_result
                best_move = possible_move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif not is_max_turn and best_value > child_result:
                best_value = child_result
                best_move = possible_move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        if new_player1.can_fences_step:
            for possible_move_fence in possible_moves_fence:
                fence = new_player1.put_fence(
                    possible_move_fence.position,
                    possible_move_fence.direction
                )
                child_result, child_move = self.minimax_tree(
                    depth + 1, new_player1, player2, alpha, beta,
                    not is_max_turn, fence
                )
                if is_max_turn and best_value < child_result:
                    best_value = child_result
                    best_move = possible_move_fence
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
                elif not is_max_turn and best_value > child_result:
                    best_value = child_result
                    best_move = possible_move_fence
                    beta = min(beta, best_value)
                    if beta <= alpha:
                        break

        # if new_player1.can_fences_step:
        #     for possible_move_fence in possible_moves_fence:
        #         new_player1.put_fence(
        #             possible_move_fence.position,
        #             possible_move_fence.direction
        #         )
        #         result = self.minimax_tree(
        #             depth + 1, new_player1, player2, self.first_n, self.last_n
        #         )
        #         alpha_beta = max(alpha_beta, result)
        #         if result >= beta:
        #             return alpha_beta
        return best_value, best_move

    def get_evaluation_function(self, new_player1: Player, player2: Player):
        fences = self.get_all_fences(new_player1, player2)
        blocked_moves = self.get_fences_blocked_moves(fences)
        a = self.calculator_controller.get_shortest_path_from_position(
            new_player1.pawn.position,
            blocked_moves,
            new_player1.end_position
        )[1]
        print(f'a = {a}')
        return a

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
