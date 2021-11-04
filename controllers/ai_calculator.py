import random
import time
from copy import deepcopy
from typing import List, Tuple

from controllers.step_calculator_controller import StepCalculatorController
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from models.player import Player
from view.fence import Fence
from view.utils import FenceDirection


class AiCalculator:

    def __init__(
        self,
        n: int,
        calculator_controller: StepCalculatorController,
        player2: Player,
    ):
        self.n = n
        self.max_depth = 2
        self.calculator_controller = calculator_controller
        self.player2 = player2

    def choose_step(self, player: Player):
        player_bot = deepcopy(player)
        start_time = time.time()
        best_value, best_move = self.minimax_tree(
            0, player_bot, self.player2, float('-inf'), float('inf'), True
        )
        print("--- %s seconds ---" % (time.time() - start_time))
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
        best_move = None
        if depth == self.max_depth:
            return self.get_evaluation_function(player_bot, player2), best_move

        possible_moves_fence, possible_moves_player_1 = \
            self.get_valid_steps_for_bot_player(
                player_bot.can_fences_step, player_bot, player2
            )

        possible_moves = self.shuffle_moves(
            player_bot, player2, possible_moves_fence, possible_moves_player_1
        )

        best_value = float('-inf') if is_max_turn else float('inf')
        for possible_move in possible_moves:
            fence = None
            if isinstance(possible_move, PawnStep):
                player_bot.move_pawn_to_position(
                    GridPosition(
                        possible_move.to_position.column,
                        possible_move.to_position.row
                    )
                )
            if isinstance(possible_move, FenceStep) and player_bot.can_fences_step:
                fence = player_bot.put_fence(
                    possible_move.position,
                    possible_move.direction
                )
            child_result, child_move = self.minimax_tree(
                depth + 1,
                player_bot,
                player2,
                alpha, beta,
                not is_max_turn
            )
            if fence:
                player_bot.fences.remove(fence)

            if is_max_turn:
                if best_value < child_result:
                    best_value = child_result
                    best_move = possible_move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif not is_max_turn:
                child_result = -child_result
                if best_value > child_result:
                    best_value = child_result
                    best_move = possible_move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

        return best_value, best_move

    def get_evaluation_function(self, player_bot: Player, player2: Player):
        fences = self.get_all_fences(player_bot, player2)
        blocked_moves = self.calculator_controller.get_fences_blocked_moves(
            fences
        )
        shortest_path_for_bot = self.calculator_controller. \
            get_shortest_path_from_position(
                player_bot.pawn.position,
                blocked_moves,
                player_bot.end_position
            )
        shortest_path_for_player = self.calculator_controller. \
            get_shortest_path_from_position(
                player2.pawn.position,
                blocked_moves,
                player2.end_position
            )

        shortest_path_from_start_to_current_for_bot = self.calculator_controller. \
            get_shortest_path_from_position(
                player_bot.start_position,
                [],
                [player_bot.pawn.position]
            )

        player_bot_row = player_bot.pawn.position.row
        if player_bot_row == player_bot.end_position[0].row:
            shortest_path_to_next_row = 0
        else:
            if player_bot.end_position[0].row == 0:
                end_next_rows_bot = [
                    GridPosition(i, player_bot.pawn.position.row - 1)
                    for i in range(self.n)
                ]
            else:
                end_next_rows_bot = [
                    GridPosition(i, player_bot.pawn.position.row + 1)
                    for i in range(self.n)
                ]

            shortest_path_to_next_row = self.calculator_controller. \
                get_shortest_path_from_position(
                    player_bot.pawn.position,
                    blocked_moves,
                    end_next_rows_bot
                )

        return (
            0.65 * (shortest_path_for_bot - shortest_path_for_player) +
            0.2 * shortest_path_to_next_row +
            0.05 * shortest_path_from_start_to_current_for_bot +
            0.1 * (len(player_bot.fences) - len(player2.fences))
        )

    @staticmethod
    def get_all_fences(player_bot: Player, player2: Player) -> List[Fence]:
        fences = []
        fences.extend(player_bot.fences)
        fences.extend(player2.fences)

        return fences

    @staticmethod
    def get_players_current_and_start_positions(
        player_bot: Player, player2: Player
    ) -> List[Tuple[GridPosition, GridPosition]]:
        return [
            (player_bot.pawn.position, player_bot.start_position),
            (player2.pawn.position, player2.start_position)
        ]

    def get_valid_steps_for_bot_player(
        self, can_fences_step: bool, player_bot: Player, player2: Player
    ) -> Tuple[List[FenceStep], List[PawnStep]]:
        fences = self.get_all_fences(player_bot, player2)
        blocked_moves = self.calculator_controller.get_fences_blocked_moves(
            fences
        )
        valid_fence_steps_around_position = []
        if can_fences_step:
            players_current_and_start_positions = \
                self.get_players_current_and_start_positions(player_bot, player2)
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
                player_bot.pawn.position,
                [(player2.pawn.position.column, player2.pawn.position.row)],
                blocked_moves
            )
        return (
            valid_fence_steps_around_position,
            valid_pawn_steps_for_player1
        )

    @staticmethod
    def shuffle_moves(
        bot_player: Player,
        player2: Player,
        possible_moves_fence: List[FenceStep],
        possible_moves_player: List[PawnStep],
    ):
        shuffled1 = []
        shuffled2 = []
        shuffled3 = []
        all_moves = [*possible_moves_player, *possible_moves_fence]
        priority = (
            True
            if player2.pawn.position.row + 5 >= player2.end_position[0].row
            else False
        )
        for move in all_moves:
            if isinstance(move, PawnStep):
                if (move.from_position.row - move.to_position.row) == 1:
                    shuffled1.insert(priority, move)
                elif (move.from_position.row - move.to_position.row) == 1:
                    shuffled3.append(move)
                else:
                    shuffled2.append(move)

            elif isinstance(move, FenceStep):
                if move.direction == FenceDirection.HORIZONTAL:
                    if bot_player.end_position[0].row == 0:
                        if player2.pawn.position.bottom().row == move.position.row:
                            shuffled1.insert(not priority, move)
                        elif player2.pawn.position.row == move.position.row:
                            shuffled3.append(move)
                        else:
                            shuffled2.append(move)
                    else:
                        if player2.pawn.position.bottom().row == move.position.row:
                            shuffled3.append(move)
                        elif player2.pawn.position.row == move.position.row:
                            shuffled1.insert(not priority, move)
                        else:
                            shuffled2.append(move)
                else:
                    shuffled2.append(move)
        random.shuffle(shuffled2)
        return [*shuffled1, *shuffled2, *shuffled3][:6]
