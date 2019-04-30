from random import randint
from Cell import Cell


class MineField:
    """Wrapper class for the minesweeper board.

    Args:
        row (int): the width of the board.
        col (int): the height of the board.

    """
    BOMB: str = '#'
    SPACE: str = ' '

    def __init__(self, row: int = 10, col: int = 10) -> None:
        self.row = row
        self.col = col
        # TODO research more effective bomb distribution ratios
        self.bomb_count = row * col // 4
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

        while bombsInGrid < self.bomb_count:
            randRow = randint(0, self.row - 1)
            randCol = randint(0, self.col - 1)

            if self.mine_field[randRow][randCol].get_type() != Cell.MINE:
                self.mine_field[randRow][randCol].set_type(Cell.MINE)
                bombsInGrid += 1
                self.increment_neighbors(randRow, randCol)

    def increment_neighbors(self, row: int, col: int):
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

                    if self.mine_field[row+i][col+j].get_type() == Cell.MINE:
                        continue

                    if self.mine_field[row+i][col+j].get_type() == Cell.EMPTY:
                        self.mine_field[row+i][col+j].set_type(Cell.NONEMPTY)

                    self.mine_field[row+i][col+j].add_mine()


def main():
    numRows = 10
    numCols = 10

    field = MineField(numRows, numCols)


if __name__ == "__main__":
    main()
