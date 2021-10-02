class GridPosition:

    def __init__(self, column, row):
        self.column = column
        self.row = row

    def left(self) -> 'GridPosition':
        return GridPosition(self.column - 1, self.row)

    def right(self):
        return GridPosition(self.column + 1, self.row)

    def top(self):
        return GridPosition(self.column, self.row - 1)

    def bottom(self):
        return GridPosition(self.column, self.row + 1)

    def clone(self):
        return GridPosition(self.column, self.row)

    def __eq__(self, other: 'GridPosition'):
        return self.column == other.column and self.row == other.row

    def __ne__(self, other: 'GridPosition'):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.column, self.row))

    def __str__(self):
        return f'GridPosition({self.column}, {self.row})'

    def __repr__(self):
        return f'GridPosition({self.column}, {self.row})'
