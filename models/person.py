from typing import Union, List

from controllers.utils import PlayerActionKey, columns_to_bot, fences_to_bot
from exception import NoWayError
from models.fence_step import FenceStep
from models.grid_position import GridPosition
from models.pawn_step import PawnStep
from models.player import Player
from view.console import Console


class Person(Player):

    def play(
        self,
        console: Console,
        valid_pawn_steps: List[PawnStep],
        valid_fence_steps: List[FenceStep],
    ) -> Union[PawnStep, FenceStep]:
        if len(valid_pawn_steps) + len(valid_fence_steps) == 0:
            raise NoWayError

        while True:
            key, value = console.get_keyboard()
            if key == PlayerActionKey.PAWN_STEP.value or key == PlayerActionKey.PAWN_JUMP.value:
                column = value[0]
                if column in columns_to_bot:
                    column = columns_to_bot[column]
                row = int(value[1])
                pawn_step = PawnStep(self.pawn.position, GridPosition(column, row-1))
                if pawn_step is not None and pawn_step in valid_pawn_steps:
                    return pawn_step
            if key == PlayerActionKey.FENCE_STEP.value and self.can_fences_step:
                fence_step = [k for k, v in fences_to_bot.items() if v == value][0]
                if fence_step is not None and fence_step in valid_fence_steps:
                    return fence_step

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name} ({self.color})'

