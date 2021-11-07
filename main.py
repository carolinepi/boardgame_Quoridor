from controllers.config_controller import Config
from controllers.game_controller import GameController
from controllers.step_calculator_controller import StepCalculatorController
from controllers.utils import PlayerActionKey
from models.ai_bot import AiBot

from models.person import Person
from models.player import ColorEnum

from view.console import Console

if __name__ == '__main__':
    color = input()
    if color == 'black':
        players = [
            Person(name='AnotherBot', color=ColorEnum.RED),
            AiBot(name='Bot', color=ColorEnum.GREEN)
        ]
    else:
        players = [
            AiBot(name='Bot', color=ColorEnum.GREEN),
            Person(name='AnotherBot', color=ColorEnum.RED)
        ]
    # config_controller = ConfigController('./config.yaml')
    config = Config(n=9, square_size=64, inner_size=8)
    board = Console(config)
    calculator_controller = StepCalculatorController(config.n)
    game = GameController(players, board, calculator_controller)
    while True:
        game.start_game()
        game.play_game()
        key = board.get_keyboard()
        if key == PlayerActionKey.RETRY_GAME.value:
            game.repeat_game()
        else:
            break
    game.finish()
