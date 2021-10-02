from controllers.config_controller import ConfigController
from controllers.game_controller import GameController
from controllers.step_calculator_controller import StepCalculatorController

from models.bot import Bot
from models.person import Person
from models.player import ColorEnum

from view.board import Board

if __name__ == '__main__':
    players = [
        Person(name='Caroline', color=ColorEnum.RED),
        Bot(name='Bot', color=ColorEnum.GREEN)
    ]
    config_controller = ConfigController('./config.yaml')
    config = config_controller.parse_config()

    board = Board(config)
    calculator_controller = StepCalculatorController(config.n)
    game = GameController(players, board, calculator_controller)
    game.init_game()
    game.play_game()
    game.finish()

