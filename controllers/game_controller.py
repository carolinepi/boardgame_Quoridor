from typing import List

from controllers.fence_step import FenceStep
from controllers.pawn_step import PawnStep
from controllers.step_calculator_controller import StepCalculatorController

from models.player import Player

from view.board import Board


class GameController:
    def __init__(
        self,
        players: List[Player],
        board: Board,
        calculator_controller: StepCalculatorController
    ):
        self.players = players
        self.board = board
        self.calculator_controller = calculator_controller

    @property
    def players_len(self) -> int:
        return len(self.players)

    def set_players_position(self):
        start_positions = self.board.get_start_positions()
        for player, start_position in zip(self.players, start_positions):
            print(f'{player.name} set in {start_position}')
            player.set_start_position(start_position)
            player.set_pawn()
            end_positions = self.board.get_end_positions(start_position)
            player.set_end_position(end_positions)

    def init_game(self):
        self.set_players_position()
        self.board.create_window()
        self.board.draw()
        for player in self.players:
            field = self.board.get_field(player.start_position)
            self.board.draw_pawn(player.pawn, field)

        finished = False
        while not finished:
            for player in self.players:
                print(f'{player} go')
                valid_pawn_steps = self.calculator_controller.get_intersection_valid_pawn_steps_for_position(player.pawn.position)
                valid_fence_steps = self.calculator_controller.get_valid_fence_steps_for_position(player.pawn.position)
                action = player.play(
                    self.board,
                    valid_pawn_steps,
                    valid_fence_steps,
                )
                if isinstance(action, PawnStep):
                    field = self.board.get_field(action.to_position)
                    player.move_pawn(field)
                    self.board.move_pawn(player.pawn, field)
                    if player.has_won:
                        finished = True
                        print(f'{player.name} is winner')
                # elif isinstance(action, FenceStep):
                #     player.placeStep(action.coord, action.direction)
                # elif isinstance(action, Quit):
                #     finished = True
                #     print("Player %s quitted" % player.name)

    def finish(self):
        self.board.close_window()
