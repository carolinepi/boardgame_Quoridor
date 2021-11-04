import random
import time
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
        calculator_controller: StepCalculatorController,
        player2: Player,
    ):
        self.max_depth = 3
        self.calculator_controller = calculator_controller
        self.player2 = player2

    def choose_step(self, player: Player):
        player_bot = player
        start_time = time.time()
        best_value, best_move = self.minimax_tree(
            0, player_bot, self.player2, float('-inf'), float('inf'), False
        )
        print("--- %s seconds ---" % (time.time() - start_time))
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
        # print(f'depth = {depth}, alpha = {alpha}, beta = {beta}, player1 = {player_bot.pawn.position}')
        best_move = None
        if depth == self.max_depth:
            print(f'if depth == self.max_depth: {self.get_evaluation_function(player_bot, player2)} {best_move}')
            return self.get_evaluation_function(player_bot, player2), best_move

        possible_moves_fence, possible_moves_player_1 = \
            self.get_valid_steps_for_bot_player(
                player_bot.can_fences_step, player_bot, player2
            )

        possible_moves = self.shuffle_moves(
            player_bot, player2, possible_moves_fence, possible_moves_player_1
        )
        print(possible_moves)

        best_value = float('-inf') if is_max_turn else float('inf')
        for possible_move in possible_moves:
            fence = None
            if isinstance(possible_move, PawnStep):
                player_bot.pawn.set_position(
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

            # print(f'is_max_turn = {is_max_turn} best_value = {best_value}, child_result = {child_result}')

            if is_max_turn:
                if best_value < child_result:
                    best_value = child_result
                    best_move = possible_move
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            elif not is_max_turn:
                if best_value > child_result:
                    best_value = child_result
                    best_move = possible_move
                beta = min(beta, best_value)
                if beta <= alpha:
                    break

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
            )
        shortest_path_for_player = self.calculator_controller. \
            get_shortest_path_from_position(
                player2.pawn.position,
                blocked_moves,
                player2.end_position
            )
        # print(f'shortest_path_for_player = {shortest_path_for_player}')
        # print(f'shortest_path_for_bot = {shortest_path_for_bot}')
        return abs(shortest_path_for_player - shortest_path_for_bot)

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
        self, can_fences_step: bool, new_player1: Player, player2: Player
    ) -> Tuple[List[FenceStep], List[PawnStep]]:
        fences = self.get_all_fences(new_player1, player2)
        blocked_moves = self.calculator_controller.get_fences_blocked_moves(
            fences
        )
        valid_fence_steps_around_position = []
        if can_fences_step:
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
        for move in all_moves:
            if isinstance(move, PawnStep):
                if (move.from_position.row - move.to_position.row) == 1:
                    shuffled1.insert(0, move)
                elif (move.from_position.row - move.to_position.row) == 1:
                    shuffled3.append(move)
                else:
                    shuffled2.append(move)

            elif isinstance(move, FenceStep):
                if move.direction == FenceDirection.HORIZONTAL:
                    if bot_player.end_position[0].row == 0:
                        if player2.pawn.position.bottom().row == move.position.row:
                            shuffled1.insert(0, move)
                        elif player2.pawn.position.row == move.position.row:
                            shuffled3.append(move)
                    else:
                        if player2.pawn.position.bottom().row == move.position.row:
                            shuffled3.append(move)
                        elif player2.pawn.position.row == move.position.row:
                            shuffled1.insert(0, move)
                else:
                    shuffled2.append(move)
        random.shuffle(shuffled1)
        if len(shuffled1) > 0:
            return [*shuffled1, *shuffled2]
        else:
            return [*shuffled2, *shuffled3]
