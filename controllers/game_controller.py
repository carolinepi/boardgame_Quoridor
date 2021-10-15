from typing import List, Tuple, Any

from graphics import GraphicsError

from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from controllers.step_calculator_controller import StepCalculatorController

from models.player import Player

from view.board import Board
from view.fence import Fence


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

    def start_game(self):
        self.set_players_position()
        for player in self.players:
            field = self.board.get_field(player.start_position)
            self.board.draw_pawn(player.pawn, field)

    def init_game_board(self):
        self.board.create_window()
        self.board.draw()

    def repeat_game(self):
        for player in self.players:
            for fence in player.fences:
                self.board.undraw_fence(fence)
            self.board.undraw_pawn(player.pawn)
            player.clean_player_data()

    def play_game(self):
        finished = False
        try:
            while not finished:
                for player in self.players:

                    players_position = self.get_players_positions(player)
                    fences = self.get_all_fences()
                    blocked_moves = self.get_fences_blocked_moves(fences)

                    players_cur_start_positions = self.\
                        get_players_current_and_start_positions()

                    valid_pawn_steps = self.calculator_controller.\
                        get_valid_pawn_steps(
                            position=player.pawn.position,
                            players_positions=players_position,
                            blocked_moves=blocked_moves
                        )

                    valid_fence_steps = self.calculator_controller.\
                        get_valid_fence_steps(
                            fences=fences,
                            blocked_moves=blocked_moves,
                            players_positions=players_cur_start_positions
                        )

                    action = player.play(
                        board=self.board,
                        valid_pawn_steps=valid_pawn_steps,
                        valid_fence_steps=valid_fence_steps,
                    )

                    if isinstance(action, PawnStep):
                        finished = self.play_pawn_step(player, action)
                        if finished:
                            break
                    elif isinstance(action, FenceStep):
                        self.play_fence_step(player, action)
        except GraphicsError:
            pass

    def play_pawn_step(
        self, player: Player, action: PawnStep
    ) -> bool:
        field = self.board.get_field(action.to_position)
        player.move_pawn(field)
        self.board.move_pawn(player.pawn, field)
        if player.has_won:
            score = player.inc_score()
            print(f'{player.name} is winner')
            print(f'Score of {player.name} = {score}')
            return True
        return False

    def play_fence_step(self, player: Player, action: FenceStep) -> None:
        field = self.board.get_field(action.position)
        fence = player.put_fence(action.position, action.direction)
        self.board.put_fence(fence, field)

    def get_players_positions(self, current_player) -> List[Tuple[int, int]]:
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

    @staticmethod
    def get_fences_blocked_moves(
        fences: List[Fence]
    ) -> List[Tuple[GridPosition, GridPosition]]:
        moves = []
        for fence in fences:
            moves.extend(fence.coordinates)

        return moves

    def get_all_fences(self) -> List[Fence]:
        fences = []
        for player in self.players:
            fences.extend(player.fences)

        return fences

    def finish(self):
        self.board.close_window()
