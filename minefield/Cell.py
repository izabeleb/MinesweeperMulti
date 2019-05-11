class Cell:
    """Wrapper class for each cell in a MineField field.

    Args:
        row (int): the row the cell is located int.
        col (in): the column the cell is located in
        mine (bool): whether the cell is a mine or not.
        flag (bool): whether teh user has marked the cell with a flag or not.
        mine_count (int): the amount of mines surrounding the cell.
        visited (bool): whether the cell has been visited when opening cells or
            not.
        clicked (bool): whether the the cell has been clicked by the user or
            not.
    """

    def __init__(self, row: int, col: int, mine: bool = False,
                 flag: bool = False, mine_count: int = 0,
                 visited: bool = False, clicked: bool = False):
        self._row: int = row
        self._col: int = col
        self._mine: bool = mine
        self._flag: bool = flag
        self._mine_count: int = mine_count
        self._visited: bool = visited
        self._clicked: bool = clicked

    def __repr__(self):
        if self._mine:
            return '#'
        else:
            return repr(self._mine_count)

    def add_mine(self) -> None:
        """Increment the amount of mines surrounding the cell."""
        self._mine_count += 1

    def get_mine_count(self) -> int:
        return self._mine_count

    def set_mine_count(self, mine_count: int) -> None:
        self._mine_count = mine_count

    def is_mine(self) -> bool:
        return self._mine

    def set_mine(self, mine) -> None:
        self._mine = mine

    def is_flag(self) -> bool:
        return self._flag

    def set_flag(self, flag) -> None:
        self._flag = flag

    def get_row(self) -> int:
        return self._row

    def get_col(self) -> int:
        return self._col

    def is_visited(self) -> bool:
        return self._visited

    def set_visited(self, visited) -> None:
        self._visited = visited

    def is_clicked(self) -> bool:
        return self._clicked

    def set_clicked(self, clicked: bool) -> None:
        self._clicked = clicked
