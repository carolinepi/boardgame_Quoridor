from graphics import Circle, Text, Point, Rectangle

from view.utils import ColorEnum

try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk


class IFacade:

    def auto_set(self, color: ColorEnum) -> None:
        raise NotImplemented()

    def draw(self, graphwin: tk.Canvas) -> None:
        raise NotImplemented()


class RectangleFacade(IFacade):

    def __init__(
        self, p1: Point, p2: Point, color: ColorEnum
    ) -> None:
        self.rectangle = Rectangle(p1, p2)
        self.auto_set(color)

    def auto_set(self, color: ColorEnum) -> None:
        self.rectangle.setFill(color.value)
        self.rectangle.setWidth(0)

    def draw(self, graphwin: tk.Canvas) -> None:
        self.rectangle.draw(graphwin)

    def undraw(self) -> None:
        self.rectangle.undraw()


class PawnFigure(IFacade):

    def __init__(
        self,
        p: Point,
        radius: int,
        label: str,
        color: ColorEnum,
        size_label: int
    ) -> None:
        self.circle = Circle(p, radius)
        self.label = Text(p, label)
        self.auto_set(color, size_label)

    def auto_set(self, color: ColorEnum, size_label: int) -> None:
        self.circle.setFill(color.value)
        self.circle.setWidth(0)
        self.label.setSize(size_label)
        self.label.setStyle("bold")
        self.label.setTextColor(ColorEnum.WHITE.value)

    def __repr__(self) -> str:
        return f'PawnFigure({self.circle.getCenter()}, ' \
               f'{self.circle.radius}, {self.label.getText()})'

    def draw(self, graphwin: tk.Canvas) -> None:
        self.circle.draw(graphwin)
        self.label.draw(graphwin)

    def undraw(self) -> None:
        self.circle.undraw()
        self.label.undraw()


class FenceFigure(RectangleFacade):

    def __repr__(self) -> str:
        return f'PawnFigure({self.rectangle.p1}, {self.rectangle.p2})'


class Background(RectangleFacade):

    def __repr__(self) -> str:
        return f'Background({self.rectangle.p1}, {self.rectangle.p2})'


class FieldFigure(RectangleFacade):

    def __repr__(self) -> str:
        return f'FieldFigure({self.rectangle.p1}, {self.rectangle.p2})'
