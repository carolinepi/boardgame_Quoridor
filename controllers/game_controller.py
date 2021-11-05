from typing import List, Tuple

from controllers.ai_calculator import AiCalculator
from exception import NoWayError
from models.ai_bot import AiBot
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from controllers.step_calculator_controller import StepCalculatorController

from models.player import Player

from view.board import Board
from view.console import Console
from view.fence import Fence
from view.utils import StepType


class GameController:
    def __init__(
        self,
        players: List[Player],
        console: Console,
        calculator_controller: StepCalculatorController
    ):
        self.players = players
        self.console = console
        self.calculator_controller = calculator_controller

    @property
    def players_len(self) -> int:
        return len(self.players)

    def set_players_position(self):
        start_positions = self.console.get_start_positions()
        for player, start_position in zip(self.players, start_positions):
            player.set_start_position(start_position)
            player.set_pawn()
            end_positions = self.console.get_end_positions(start_position)
            player.set_end_position(end_positions)

    def start_game(self):
        self.set_players_position()
        for player in self.players:
            field = self.console.get_field(player.start_position)
            # self.console.draw_pawn(player.pawn, field)

    # def init_game_board(self):
    #     self.console.create_window()
    #     self.console.draw()

    def init_game_board(self):
        pass

    def repeat_game(self):
        for player in self.players:
            # for fence in player.fences:
                # self.console.undraw_fence(fence)
            # self.console.undraw_pawn(player.pawn)
            player.clean_player_data()

    def play_game(self):
        finished = False
        try:
            while not finished:
                for player in self.players:
                    if isinstance(player, AiBot):
                        another_player_set = list(set(self.players) - {player})
                        ai_calculator = AiCalculator(
                            self.console.n,
                            self.calculator_controller,
                            another_player_set[0]
                        )
                        step = player.play_ai(ai_calculator)
                    else:
                        players_position = self.get_players_positions(player)
                        fences = self.get_all_fences()
                        blocked_moves = self.calculator_controller.\
                            get_fences_blocked_moves(fences)
                        players_current_and_start_positions = \
                            self.get_players_current_and_start_positions()

                        valid_pawn_steps = self.calculator_controller.\
                            get_valid_pawn_steps(
                                player.pawn.position,
                                players_position,
                                blocked_moves
                            )

                        valid_fence_steps = self.calculator_controller.\
                            get_valid_fence_steps(
                                fences,
                                blocked_moves,
                                players_current_and_start_positions
                            )

                        step = player.play(
                            self.console,
                            valid_pawn_steps,
                            valid_fence_steps,
                        )

                    print_result = False
                    if isinstance(player, AiBot):
                        print_result = True
                    if isinstance(step, PawnStep):
                        finished = self.play_pawn_step(player, step, print_result)
                        if finished:
                            break
                    elif isinstance(step, FenceStep):
                        self.play_fence_step(player, step, print_result)
        except Exception:
            pass

    def play_pawn_step(
        self, player: Player, step: PawnStep, print_result: bool
    ) -> bool:
        field = self.console.get_field(step.to_position)
        if print_result:
            if step.step_type == StepType.MOVE:
                player.move_pawn(field)
            elif step.step_type == StepType.JUMP:
                player.jump_pawn(field)
        else:
            player.move_pawn_to_position(field.position)
        if player.has_won:
            score = player.inc_score()
            return True
        return False

    def play_fence_step(self, player: Player, step: FenceStep, print_result: bool) -> None:
        field = self.console.get_field(step.position)
        if print_result:
            fence = player.put_fence_with_print(step.position, step.direction)
        else:
            fence = player.put_fence(step.position, step.direction)
        # self.console.put_fence(fence, field)

    def get_players_positions(
        self, current_player: Player
    ) -> List[Tuple[int, int]]:
        return [
            (player.pawn.position.column, player.pawn.position.row)
            for player in self.players if player != current_player
        ]

    def get_players_current_and_start_positions(
        self
    ) -> List[Tuple[GridPosition, GridPosition]]:
        return [
            (player.pawn.position, player.start_position)
            for player in self.players
        ]

    def get_all_fences(self) -> List[Fence]:
        fences = []
        for player in self.players:
            fences.extend(player.fences)

        return fences

    def finish(self):
        self.console.exit()
