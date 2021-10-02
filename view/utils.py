from enum import Enum
from typing import Tuple, Union


class Color:
    def __init__(self, value: str):
        self.value = value


class ColorEnum(Enum):
    RED = "#c0392b"
    BLUE = "#2980b9"
    GREEN = "#27ae60"
    ORANGE = "#f39c12"
    PURPLE = "#8e44ad"
    TURQUOISE = "#16a085"
    WHITE = "#ffffff"
    BLACK = "#000000"
    SQUARE = "#eeeeee"

    @staticmethod
    def to_rgb(r: str, g: str, b: str) -> str:
        return f'#{r}{g}{b}'

    @staticmethod
    def get_values(color: str) -> Tuple[int, ...]:
        r_slice = slice(1, 3)
        g_slice = slice(3, 5)
        b_slice = slice(5, 7)
        return (
            int(color[r_slice], 16),
            int(color[g_slice], 16),
            int(color[b_slice], 16),
        )

    @staticmethod
    def get_mixed_ratio(value1: int, value2: int):
        ratio = 0.5
        return int(ratio * value1 + (1 - ratio) * value2)

    @classmethod
    def mix_colors(cls, color1: 'ColorEnum', color2: 'ColorEnum'):
        r1, g1, b1 = cls.get_values(color1.value)
        r2, g2, b2 = cls.get_values(color2.value)
        r, g, b = map(cls.get_mixed_ratio, [r1, g1, b1], [r2, g2, b2])
        return Color(cls.to_rgb(r, g, b))


ColorType = Union[Color, ColorEnum]


class FenceDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
