from enum import Enum
from view.utils import FenceDirection


# class PlayerActionKey(Enum):
#     PAWN_STEP = 'q'
#     FENCE_STEP = 'e'
#     RETRY_GAME = 'Return'


class PlayerActionKey(Enum):
    PAWN_STEP = 'move'
    PAWN_JUMP = 'jump'
    FENCE_STEP = 'wall'
    RETRY_GAME = 'Return'


directions = {
    'v': FenceDirection.VERTICAL,
    'h': FenceDirection.HORIZONTAL
}

directions_to_string = {
    FenceDirection.VERTICAL: 'v',
    FenceDirection.HORIZONTAL: 'h'
}
