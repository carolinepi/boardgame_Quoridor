from view.board import Board
from controllers.game_controller import GameController
from models.bot import Bot
from models.person import Person
from models.player import Color

if __name__ == '__main__':
    players = [
        Person(name='Caroline', color=Color.RED),
        Bot(name='Bot', color=Color.GREEN)
    ]
    board = Board()
    game = GameController(players, board)
    game.init_game()
    game.finish()

