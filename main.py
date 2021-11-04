from controllers.config_controller import ConfigController
from controllers.game_controller import GameController
from controllers.step_calculator_controller import StepCalculatorController
from controllers.utils import PlayerActionKey
from models.ai_bot import AiBot

from models.bot import Bot
from models.person import Person
from models.player import ColorEnum

from view.board import Board

if __name__ == '__main__':
    players = [
        Person(name='Caroline', color=ColorEnum.RED),
        AiBot(name='Bot', color=ColorEnum.GREEN)
    ]
    config_controller = ConfigController('./config.yaml')
    config = config_controller.parse_config()

    board = Board(config)
    calculator_controller = StepCalculatorController(config.n)
    game = GameController(players, board, calculator_controller)
    game.init_game_board()
    while True:
        game.start_game()
        game.play_game()
        key = board.get_keyboard()
        if key == PlayerActionKey.RETRY_GAME.value:
            game.repeat_game()
        else:
            break
    game.finish()
