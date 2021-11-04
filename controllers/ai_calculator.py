import random
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
        calculator_controller: StepCalculatorController,
        player2: Player,
    ):
        self.max_depth = 2
        self.calculator_controller = calculator_controller
        self.player2 = player2

    def choose_step(self, player: Player):
        player_bot = player

        best_value, best_move = self.minimax_tree(
            0, player_bot, self.player2, float('-inf'), float('inf'), True
        )
        print(f'FINAL: {best_value}')
        return best_move

    def minimax_tree(
        self,
        depth: int,
        player_bot: Player,
        player2: Player,
        alpha: float,
        beta: float,
        is_max_turn: bool,
    ):
        print(f'depth = {depth}, alpha = {alpha}, beta = {beta}, player1 = {player_bot.pawn.position}')
        best_move = None
        if depth == self.max_depth:
            print(f'if depth == self.max_depth: {self.get_evaluation_function(player_bot, player2)} {best_move}')
            return self.get_evaluation_function(player_bot, player2), best_move

        possible_moves_fence, possible_moves_player_1, _ = \
            self.get_valid_steps_for_bot_player(player_bot, player2)
        random.shuffle(possible_moves_player_1)
        random.shuffle(possible_moves_fence)
        print(f'possible_moves_player_1 {possible_moves_player_1}')
        print(f'possible_moves_fence {possible_moves_fence}')
        best_value = float('-inf') if is_max_turn else float('inf')
        for possible_move in possible_moves_player_1:
            player_bot.pawn.set_position(
                GridPosition(
                    possible_move.to_position.column,
                    possible_move.to_position.row
                )
            )
            child_result, child_move = self.minimax_tree(
                depth + 1,
                player_bot,
                player2,
                alpha, beta,
                not is_max_turn
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

        # if player_bot.can_fences_step:
        #     for possible_move_fence in possible_moves_fence:
        #         fence = player_bot.put_fence(
        #             possible_move_fence.position,
        #             possible_move_fence.direction
        #         )
        #         child_result, child_move = self.minimax_tree(
        #             depth + 1,
        #             player_bot,
        #             player2,
        #             alpha, beta,
        #             not is_max_turn,
        #         )
        #         player_bot.fences.remove(fence)
        #
        #         if is_max_turn and best_value < child_result:
        #             best_value = child_result
        #             best_move = possible_move_fence
        #             alpha = max(alpha, best_value)
        #             if beta <= alpha:
        #                 break
        #
        #         elif not is_max_turn and best_value > child_result:
        #             best_value = child_result
        #             best_move = possible_move_fence
        #             beta = min(beta, best_value)
        #             if beta <= alpha:
        #                 break

        return best_value, best_move


    def get_evaluation_function(self, new_player1: Player, player2: Player):
        fences = self.get_all_fences(new_player1, player2)
        blocked_moves = self.calculator_controller.get_fences_blocked_moves(
            fences
        )
        shortest_path_for_bot = self.calculator_controller. \
            get_shortest_path_from_position(
                new_player1.pawn.position,
                blocked_moves,
                new_player1.end_position
            )[1]
        shortest_path_for_player = self.calculator_controller. \
            get_shortest_path_from_position(
                player2.pawn.position,
                blocked_moves,
                player2.end_position
            )[1]
        print(f'shortest_path_for_bot = {shortest_path_for_bot}')
        print(f'shortest_path_for_player = {shortest_path_for_player}')
        return shortest_path_for_player - shortest_path_for_bot

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

    def get_valid_steps_for_bot_player(
        self, new_player1: Player, player2: Player
    ) -> Tuple[List[FenceStep], List[PawnStep], List[PawnStep]]:
        fences = self.get_all_fences(new_player1, player2)
        blocked_moves = self.calculator_controller.get_fences_blocked_moves(
            fences
        )
        players_current_and_start_positions = \
            self.get_players_current_and_start_positions(new_player1, player2)
        valid_fence_steps = self.calculator_controller.get_valid_fence_steps(
            fences,
            blocked_moves,
            players_current_and_start_positions
        )
        valid_fence_steps_around_position = self.calculator_controller.\
            get_valid_fences_around_position(
                player2.pawn.position, valid_fence_steps
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
                [(
                    new_player1.pawn.position.column,
                    new_player1.pawn.position.row
                )],
                blocked_moves
            )
        return (
            valid_fence_steps_around_position,
            valid_pawn_steps_for_player1,
            valid_pawn_steps_for_player2,
        )
