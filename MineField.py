from random import randint
from Cell import Cell


class MineField:
    """Wrapper class for the minesweeper board.

    Args:
        row (int): the width of the board.
        col (int): the height of the board.

    """
    def __init__(self, row: int = 10, col: int = 10) -> None:
        self.row = row
        self.col = col
        # TODO research more effective bomb distribution ratios
        self.mine_count = row * col // 4
        self.mine_field = [
            [Cell(r, c) for c in range(self.col)]
            for r in range(self.row)
        ]

        self.generate_mines()

    def __repr__(self) -> str:
        repr_list: list = list()
        for i in range(self.row):
            repr_list.append(
                ' '.join([repr(cell) for cell in self.mine_field[i]])
            )
        return '\n'.join(repr_list)

    def generate_mines(self) -> None:
        """Populate the mine field with mines"""
        bombsInGrid = 0

        while bombsInGrid < self.mine_count:
            randRow = randint(0, self.row - 1)
            randCol = randint(0, self.col - 1)

            if not self.mine_field[randRow][randCol].is_mine():
                self.mine_field[randRow][randCol].set_mine()
                self.increment_neighbors(randRow, randCol)
                bombsInGrid += 1

    def increment_neighbors(self, row: int, col: int) -> None:
        """Increment the amount of bombs round the neighbor cells by one.
        Args:
            row (int): the row of the target cell.
            col (int): the column of thetarget cell.
        """
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if -1 < row + i < self.row and -1 < col + j < self.col:
                    if self.mine_field[row + i][col + j].is_mine():
                        continue

                    self.mine_field[row + i][col + j].add_mine()

    def get_row(self) -> int:
        return self.row

    def get_col(self) -> int:
        return self.col

    def get_cell_at(self, row: int, col: int) -> 'Cell':
        return self.mine_field[row][col]
