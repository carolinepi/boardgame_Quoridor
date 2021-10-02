from graphics import Circle, Text, Point, Rectangle

from view.utils import ColorEnum, ColorType


class PawnFigure:

    def __init__(
        self,
        center: Point,
        radius: int,
        label: str,
        color: ColorType,
        size_label: int
    ):
        self.circle = Circle(center, radius)
        self.label = Text(center, label)
        self.auto_set(color, size_label)

    def auto_set(self, color: ColorType, size_label: int):
        self.circle.setFill(color.value)
        self.circle.setWidth(0)
        self.label.setSize(size_label)
        self.label.setStyle("bold")
        self.label.setTextColor(ColorEnum.WHITE.value)

    def __repr__(self):
        return f'PawnFigure({self.circle.getCenter()}, ' \
               f'{self.circle.radius}, {self.label.getText()})'

    def draw(self, graphwin):
        self.circle.draw(graphwin)
        self.label.draw(graphwin)

    def undraw(self):
        self.circle.undraw()
        self.label.undraw()


class FenceFigure:

    def __init__(
        self, p1: Point, p2: Point, color: ColorType
    ):
        self.rectangle = Rectangle(p1, p2)
        self.auto_set(color)

    def auto_set(self, color: ColorType):
        self.rectangle.setFill(color.value)
        self.rectangle.setWidth(0)

    def __repr__(self):
        return f'PawnFigure({self.rectangle.p1}, {self.rectangle.p2})'

    def draw(self, graphwin):
        self.rectangle.draw(graphwin)

    def undraw(self):
        self.rectangle.undraw()
