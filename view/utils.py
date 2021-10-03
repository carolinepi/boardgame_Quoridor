from enum import Enum, auto
from typing import List, Any


class AutoNameEnum(Enum):
    def _generate_next_value_(name: str, *args: List[Any]) -> str:
        return name.lower()


class ColorEnum(AutoNameEnum):
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    ORANGE = auto()
    PURPLE = auto()
    TURQUOISE = auto()
    WHITE = auto()
    BLACK = auto()
    SNOW = auto()


class FenceDirection(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()
