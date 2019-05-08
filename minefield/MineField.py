from random import randint
from minefield import Cell
import json


class BadField(Exception):
    """Raised when a field is corrupted or malformed."""
    pass


class MineField:
    """Wrapper class for the minesweeper board.

    If mine field is specified the values of row and col are ignored,
    and the size of the mine field is determined based off of the field.

    Args:
        row (int): the width of the board.
        col (int): the height of the board.
        mine_field (list): a predefined mine_field 2-D array for

    """
    @staticmethod
    def decode(field: bytes, encoding: str = 'ascii') -> 'MineField':
        """Decode the encoded JSON representation of a MineField instnace.

        Args:
            field (bytes): the encoded representation of a mIneField object.
            encoding (str): the encoding format to decode by.

        Returns:
            (MineField): the decoded MIneField instance.
        """
        field: str = field.decode(encoding)
        field_json: dict = json.loads(field)

        max_cols: int = field_json['COLS']
        max_rows: int = field_json['ROWS']
        cell_list: list = field_json['CELLS']
        mine_field: list = [
            [None for j in range(max_cols)] for i in range(max_rows)
        ]

        for cell in cell_list:
            col = cell['COL']
            row = cell['ROW']
            mine_field[row][col] = Cell(row, col, cell['IS_MINE'],
                                        cell['IS_FLAG'], cell['MINE_COUNT'],
                                        cell['IS_VISITED'], cell['IS_CLICKED'])

        if len(mine_field) != max_rows:
            raise BadField

        for row in mine_field:
            if len(row) != max_cols:
                raise BadField

        return MineField(mine_field=mine_field)

    def __init__(self, row: int = 10, col: int = 10,
                 mine_field: list = None) -> None:
        if mine_field is not None:
            self._mine_field = mine_field
            self._max_row = len(self._mine_field)
            self._max_col = len(self._mine_field[0])
        else:
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

    def encode(self, encoding: str = 'ascii') -> bytes:
        """Encode a minefield object.

        Args:
            encoding (str)): the format to use when encoding.

        Returns:
            (bytes): the encoded JSON representation of the MineField instance.
        """

        json_dict: dict = {'COLS': self._max_col,
                           'ROWS': self._max_row,
                           'CELLS': []}
        for cell in self:
            cell_dict = {'COL': cell.get_col(),
                         'ROW': cell.get_row(),
                         'MINE_COUNT': cell.get_mine_count(),
                         'IS_MINE': cell.is_mine(),
                         'IS_FLAG': cell.is_flag(),
                         'IS_VISITED': cell.is_visited(),
                         'IS_CLICKED': cell.is_clicked()}
            json_dict['CELLS'].append(cell_dict)
        json_str: str = json.dumps(json_dict)

        return json_str.encode(encoding)

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
