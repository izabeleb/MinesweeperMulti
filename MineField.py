from random import randint
from Cell import Cell


class MineField:
    """Wrapper class for the minesweeper board.

    Args:
        row (int): the width of the board.
        col (int): the height of the board.

    """
    def __init__(self, row: int = 10, col: int = 10) -> None:
        self._max_row = row
        self._max_col = col
        # TODO research more effective bomb distribution ratios
        self._mine_count = row * col // 4
        self._mine_field = [
            [Cell(r, c) for c in range(self._max_col)]
            for r in range(self._max_row)
        ]

        self._generate_mines()

    def __repr__(self) -> str:
        repr_list: list = list()
        for i in range(self._max_row):
            repr_list.append(
                ' '.join([repr(cell) for cell in self._mine_field[i]])
            )
        return '\n'.join(repr_list)

    def __iter__(self):
        for row in self._mine_field:
            for cell in row:
                yield cell

    def _generate_mines(self) -> None:
        """Populate the mine field with mines"""
        bombsInGrid = 0

        while bombsInGrid < self._mine_count:
            randRow = randint(0, self._max_row - 1)
            randCol = randint(0, self._max_col - 1)

            if not self._mine_field[randRow][randCol].is_mine():
                self._mine_field[randRow][randCol].set_mine()
                self._increment_neighbors(randRow, randCol)
                bombsInGrid += 1

    def _increment_neighbors(self, row: int, col: int) -> None:
        """Increment the amount of bombs round the neighbor cells by one.
        Args:
            row (int): the row of the target cell.
            col (int): the column of thetarget cell.
        """
        for i in range(-1, 2):
            if not -1 < row + i < self._max_row:
                continue
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                if -1 < col + j < self._max_col:
                    if self._mine_field[row + i][col + j].is_mine():
                        continue

                    self._mine_field[row + i][col + j].add_mine()

    def surrounding_cells(self, cell: Cell) -> Cell:
        """Generator for cells surrounding the target cell.

        Args:
            cell (Cell): the cell to use as the center.

        Returns:
            (list): a list of all open and connected cells.
        """
        cell_row: int = cell.get_row()
        cell_col: int = cell.get_col()

        for i in range(-1, 2):
            if not -1 < cell_row + i < self._max_row:
                continue
            for j in range(-1, 2):
                if i == j == 0 or not -1 < cell_col + j < self._max_col:
                    continue

                yield self.get_cell_at(cell.get_row() + i, cell.get_col() + j)

    def cell_is_safe(self, cell: Cell) -> bool:
        mines_found: int = 0

        for c in self.surrounding_cells(cell):
            if c.is_flag():
                mines_found += 1

        return cell.get_mine_count() == mines_found

    def get_row(self) -> int:
        return self._max_row

    def get_col(self) -> int:
        return self._max_col

    def get_cell_at(self, row: int, col: int) -> 'Cell':
        return self._mine_field[row][col]
