from typing import Optional, Union, List

from controllers.ai_calculator import AiCalculator
from models.fence_step import FenceStep
from models.pawn_step import PawnStep
from models.player import Player


class AiBot(Player):

    def play_ai(
        self,
        ai_calculator: AiCalculator,
    ) -> Optional[Union[PawnStep, FenceStep]]:
        return ai_calculator.choose_step(self)

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name} ({self.color})'
