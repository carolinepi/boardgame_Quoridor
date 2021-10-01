from typing import List

from view.board import Board
from models.player import Player


class GameController:
    def __init__(self, players: List[Player], board: Board):
        self.players = players
        self.board = board

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
            field = self.board.get_field(player.startPosition)
            self.board.draw_pawn(player.pawn, field)

        finished = False
        while not finished:
            pass

    def finish(self):
        self.board.close_window()
