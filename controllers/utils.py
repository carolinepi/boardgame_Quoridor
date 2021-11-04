from enum import Enum

from models.fence_step import FenceStep
from models.grid_position import GridPosition
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

columns_to_bot = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
}

bots_to_columns = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I'
}


fences_to_bot = {
    FenceStep(GridPosition(1, 0), FenceDirection.VERTICAL): "S1v",
    FenceStep(GridPosition(2, 0), FenceDirection.VERTICAL): "T1v",
    FenceStep(GridPosition(3, 0), FenceDirection.VERTICAL): "U1v",
    FenceStep(GridPosition(4, 0), FenceDirection.VERTICAL): "V1v",
    FenceStep(GridPosition(5, 0), FenceDirection.VERTICAL): "W1v",
    FenceStep(GridPosition(6, 0), FenceDirection.VERTICAL): "X1v",
    FenceStep(GridPosition(7, 0), FenceDirection.VERTICAL): "Y1v",
    FenceStep(GridPosition(7, 0), FenceDirection.VERTICAL): "Y1v",
    FenceStep(GridPosition(8, 0), FenceDirection.VERTICAL): "Z1v",
    FenceStep(GridPosition(0, 1), FenceDirection.HORIZONTAL): "S1h",
    FenceStep(GridPosition(1, 1), FenceDirection.HORIZONTAL): "T1h",
    FenceStep(GridPosition(1, 1), FenceDirection.VERTICAL): "S2v",
    FenceStep(GridPosition(2, 1), FenceDirection.HORIZONTAL): "U1h",
    FenceStep(GridPosition(2, 1), FenceDirection.VERTICAL): "T2v",
    FenceStep(GridPosition(3, 1), FenceDirection.HORIZONTAL): "V1h",
    FenceStep(GridPosition(3, 1), FenceDirection.VERTICAL): "U2v",
    FenceStep(GridPosition(4, 1), FenceDirection.HORIZONTAL): "W1h",
    FenceStep(GridPosition(4, 1), FenceDirection.VERTICAL): "V2v",
    FenceStep(GridPosition(5, 1), FenceDirection.HORIZONTAL): "X1h",
    FenceStep(GridPosition(5, 1), FenceDirection.VERTICAL): "W2v",
    FenceStep(GridPosition(6, 1), FenceDirection.HORIZONTAL): "Y1h",
    FenceStep(GridPosition(6, 1), FenceDirection.VERTICAL): "X2v",
    FenceStep(GridPosition(7, 1), FenceDirection.HORIZONTAL): "Z1h",
    FenceStep(GridPosition(7, 1), FenceDirection.VERTICAL): "Y2v",
    FenceStep(GridPosition(8, 1), FenceDirection.VERTICAL): "Z2v",
    FenceStep(GridPosition(0, 2), FenceDirection.HORIZONTAL): "S2h",
    FenceStep(GridPosition(1, 2), FenceDirection.HORIZONTAL): "T2h",
    FenceStep(GridPosition(1, 2), FenceDirection.VERTICAL): "S3v",
    FenceStep(GridPosition(2, 2), FenceDirection.HORIZONTAL): "U2h",
    FenceStep(GridPosition(2, 2), FenceDirection.VERTICAL): "T3v",
    FenceStep(GridPosition(3, 2), FenceDirection.HORIZONTAL): "V2h",
    FenceStep(GridPosition(3, 2), FenceDirection.VERTICAL): "U3v",
    FenceStep(GridPosition(4, 2), FenceDirection.HORIZONTAL): "W2h",
    FenceStep(GridPosition(4, 2), FenceDirection.VERTICAL): "V3v",
    FenceStep(GridPosition(5, 2), FenceDirection.HORIZONTAL): "X2h",
    FenceStep(GridPosition(5, 2), FenceDirection.VERTICAL): "W3v",
    FenceStep(GridPosition(6, 2), FenceDirection.HORIZONTAL): "Y2h",
    FenceStep(GridPosition(6, 2), FenceDirection.VERTICAL): "X3v",
    FenceStep(GridPosition(7, 2), FenceDirection.HORIZONTAL): "Z2h",
    FenceStep(GridPosition(7, 2), FenceDirection.VERTICAL): "Y3v",
    FenceStep(GridPosition(8, 2), FenceDirection.VERTICAL): "Z3v",
    FenceStep(GridPosition(0, 3), FenceDirection.HORIZONTAL): "S3h",
    FenceStep(GridPosition(1, 3), FenceDirection.HORIZONTAL): "T3h",
    FenceStep(GridPosition(1, 3), FenceDirection.VERTICAL): "S4v",
    FenceStep(GridPosition(2, 3), FenceDirection.HORIZONTAL): "U3h",
    FenceStep(GridPosition(2, 3), FenceDirection.VERTICAL): "T4v",
    FenceStep(GridPosition(3, 3), FenceDirection.HORIZONTAL): "V3h",
    FenceStep(GridPosition(3, 3), FenceDirection.VERTICAL): "U4v",
    FenceStep(GridPosition(4, 3), FenceDirection.HORIZONTAL): "W3h",
    FenceStep(GridPosition(4, 3), FenceDirection.VERTICAL): "V4v",
    FenceStep(GridPosition(5, 3), FenceDirection.HORIZONTAL): "X3h",
    FenceStep(GridPosition(5, 3), FenceDirection.VERTICAL): "W4v",
    FenceStep(GridPosition(6, 3), FenceDirection.HORIZONTAL): "Y3h",
    FenceStep(GridPosition(6, 3), FenceDirection.VERTICAL): "X4v",
    FenceStep(GridPosition(7, 3), FenceDirection.HORIZONTAL): "Z3h",
    FenceStep(GridPosition(7, 3), FenceDirection.VERTICAL): "Y4v",
    FenceStep(GridPosition(8, 3), FenceDirection.VERTICAL): "Z4v",
    FenceStep(GridPosition(0, 4), FenceDirection.HORIZONTAL): "S4h",
    FenceStep(GridPosition(1, 4), FenceDirection.HORIZONTAL): "T4h",
    FenceStep(GridPosition(1, 4), FenceDirection.VERTICAL): "S5v",
    FenceStep(GridPosition(2, 4), FenceDirection.HORIZONTAL): "U4h",
    FenceStep(GridPosition(2, 4), FenceDirection.VERTICAL): "T5v",
    FenceStep(GridPosition(3, 4), FenceDirection.HORIZONTAL): "V4h",
    FenceStep(GridPosition(3, 4), FenceDirection.VERTICAL): "U5v",
    FenceStep(GridPosition(4, 4), FenceDirection.HORIZONTAL): "W4h",
    FenceStep(GridPosition(4, 4), FenceDirection.VERTICAL): "V5v",
    FenceStep(GridPosition(5, 4), FenceDirection.HORIZONTAL): "X4h",
    FenceStep(GridPosition(5, 4), FenceDirection.VERTICAL): "W5v",
    FenceStep(GridPosition(6, 4), FenceDirection.HORIZONTAL): "Y4h",
    FenceStep(GridPosition(6, 4), FenceDirection.VERTICAL): "X5v",
    FenceStep(GridPosition(7, 4), FenceDirection.HORIZONTAL): "Z4h",
    FenceStep(GridPosition(7, 4), FenceDirection.VERTICAL): "Y5v",
    FenceStep(GridPosition(8, 4), FenceDirection.VERTICAL): "Z5v",
    FenceStep(GridPosition(0, 5), FenceDirection.HORIZONTAL): "S5h",
    FenceStep(GridPosition(1, 5), FenceDirection.HORIZONTAL): "T5h",
    FenceStep(GridPosition(1, 5), FenceDirection.VERTICAL): "S6v",
    FenceStep(GridPosition(2, 5), FenceDirection.HORIZONTAL): "U5h",
    FenceStep(GridPosition(2, 5), FenceDirection.VERTICAL): "T6v",
    FenceStep(GridPosition(3, 5), FenceDirection.HORIZONTAL): "V5h",
    FenceStep(GridPosition(3, 5), FenceDirection.VERTICAL): "U6v",
    FenceStep(GridPosition(4, 5), FenceDirection.HORIZONTAL): "W5h",
    FenceStep(GridPosition(4, 5), FenceDirection.VERTICAL): "V6v",
    FenceStep(GridPosition(5, 5), FenceDirection.HORIZONTAL): "X5h",
    FenceStep(GridPosition(5, 5), FenceDirection.VERTICAL): "W6v",
    FenceStep(GridPosition(6, 5), FenceDirection.HORIZONTAL): "Y5h",
    FenceStep(GridPosition(6, 5), FenceDirection.VERTICAL): "X6v",
    FenceStep(GridPosition(7, 5), FenceDirection.HORIZONTAL): "Z5h",
    FenceStep(GridPosition(7, 5), FenceDirection.VERTICAL): "Y6v",
    FenceStep(GridPosition(8, 5), FenceDirection.VERTICAL): "Z6v",
    FenceStep(GridPosition(0, 6), FenceDirection.HORIZONTAL): "S6h",
    FenceStep(GridPosition(1, 6), FenceDirection.HORIZONTAL): "T6h",
    FenceStep(GridPosition(1, 6), FenceDirection.VERTICAL): "S7v",
    FenceStep(GridPosition(2, 6), FenceDirection.HORIZONTAL): "U6h",
    FenceStep(GridPosition(2, 6), FenceDirection.VERTICAL): "T7v",
    FenceStep(GridPosition(3, 6), FenceDirection.HORIZONTAL): "V6h",
    FenceStep(GridPosition(3, 6), FenceDirection.VERTICAL): "U7v",
    FenceStep(GridPosition(4, 6), FenceDirection.HORIZONTAL): "W6h",
    FenceStep(GridPosition(4, 6), FenceDirection.VERTICAL): "V7v",
    FenceStep(GridPosition(5, 6), FenceDirection.HORIZONTAL): "X6h",
    FenceStep(GridPosition(5, 6), FenceDirection.VERTICAL): "W7v",
    FenceStep(GridPosition(6, 6), FenceDirection.HORIZONTAL): "Y6h",
    FenceStep(GridPosition(6, 6), FenceDirection.VERTICAL): "X7v",
    FenceStep(GridPosition(7, 6), FenceDirection.HORIZONTAL): "Z6h",
    FenceStep(GridPosition(7, 6), FenceDirection.VERTICAL): "Y7v",
    FenceStep(GridPosition(8, 6), FenceDirection.VERTICAL): "Z7v",
    FenceStep(GridPosition(0, 7), FenceDirection.HORIZONTAL): "S7h",
    FenceStep(GridPosition(1, 7), FenceDirection.HORIZONTAL): "T7h",
    FenceStep(GridPosition(1, 7), FenceDirection.VERTICAL): "S8v",
    FenceStep(GridPosition(2, 7), FenceDirection.HORIZONTAL): "U7h",
    FenceStep(GridPosition(2, 7), FenceDirection.VERTICAL): "T8v",
    FenceStep(GridPosition(3, 7), FenceDirection.HORIZONTAL): "V7h",
    FenceStep(GridPosition(3, 7), FenceDirection.VERTICAL): "U8v",
    FenceStep(GridPosition(4, 7), FenceDirection.HORIZONTAL): "W7h",
    FenceStep(GridPosition(4, 7), FenceDirection.VERTICAL): "V8v",
    FenceStep(GridPosition(5, 7), FenceDirection.HORIZONTAL): "X7h",
    FenceStep(GridPosition(5, 7), FenceDirection.VERTICAL): "W8v",
    FenceStep(GridPosition(6, 7), FenceDirection.HORIZONTAL): "Y7h",
    FenceStep(GridPosition(6, 7), FenceDirection.VERTICAL): "X8v",
    FenceStep(GridPosition(7, 7), FenceDirection.HORIZONTAL): "Z7h",
    FenceStep(GridPosition(7, 7), FenceDirection.VERTICAL): "Y8v",
    FenceStep(GridPosition(8, 7), FenceDirection.VERTICAL): "Z8v",
    FenceStep(GridPosition(0, 8), FenceDirection.HORIZONTAL): "S8h",
    FenceStep(GridPosition(1, 8), FenceDirection.HORIZONTAL): "T8h",
    FenceStep(GridPosition(2, 8), FenceDirection.HORIZONTAL): "U8h",
    FenceStep(GridPosition(3, 8), FenceDirection.HORIZONTAL): "V8h",
    FenceStep(GridPosition(4, 8), FenceDirection.HORIZONTAL): "W8h",
    FenceStep(GridPosition(5, 8), FenceDirection.HORIZONTAL): "X8h",
    FenceStep(GridPosition(6, 8), FenceDirection.HORIZONTAL): "Y8h",
    FenceStep(GridPosition(7, 8), FenceDirection.HORIZONTAL): "Z8h"
}

