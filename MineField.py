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
        self._flagged_count = 0
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
                self._mine_field[randRow][randCol].set_mine(True)
                self._increment_neighbors(self.get_cell_at(randRow, randCol))
                bombsInGrid += 1

    def _increment_neighbors(self, cell: Cell) -> None:
        """Increment the amount of mines areound the target cell by one.

        Args:
            cell (Cell): the target cell.
        """
        for c in self.surrounding_cells(cell):
            c.set_mine_count(c.get_mine_count() + 1)

    def _decrement_neighbors(self, cell: Cell) -> None:
        """Decrement th amount of mines around the target cell by one.

        Args:
            cell (Cell): the target cell.
        """
        for c in self.surrounding_cells(cell):
            c.set_mine_count(c.get_mine_count() - 1)

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
        """Determine if a cell should be considered safe.

        A cell is considered safe if it has an equal number of mines around it
        as flags placed by the player.

        Args:
            cell (Cell): the cell to test for safety.

        Returns:
            (bool): True is safe, False otherwise.
        """
        if cell.get_mine_count() == 0:
            return True

        mines_found: int = 0

        for c in self.surrounding_cells(cell):
            if c.is_flag():
                mines_found += 1

        return cell.get_mine_count() == mines_found

    def field_is_safe(self) -> bool:
        """Check if every mine in the field has been flagged.

        Returns:
            (bool): Ture iss evey mine has been flagged, False otherwise.
        """
        for cell in self:
            if cell.is_mine() and not cell.is_flag():
                return False
        return True

    def get_row(self) -> int:
        return self._max_row

    def get_col(self) -> int:
        return self._max_col
    
    def add_flagged(self):
        self._flagged_count += 1
        
    def subtract_flagged(self):
        self._flagged_count -= 1
    
    def get_flagged_count(self) -> int:
        return self._flagged_count
    
    def get_mine_count(self) -> int:
        return self._mine_count

    def get_cell_at(self, row: int, col: int) -> 'Cell':
        return self._mine_field[row][col]

    def move_mine(self, cell: Cell) -> None:
        randRow = randint(0, self._max_row - 1)
        randCol = randint(0, self._max_col - 1)

        while self._mine_field[randRow][randCol].is_mine():
            randRow = randint(0, self._max_row - 1)
            randCol = randint(0, self._max_col - 1)

        self._mine_field[randRow][randCol].set_mine(True)
        cell.set_mine(False)
