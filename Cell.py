class Cell:
    """Wrapper class for each cell in a MineField field."""

    def __init__(self, row: int, col: int):
        self._row: int = row
        self._col: int = col
        self._mine: bool = False
        self._flag: bool = False
        self._mine_count: int = 0
        self._visited: bool = False
        self._clicked: bool = False

    def __repr__(self):
        if self._mine:
            return '#'
        else:
            return repr(self._mine_count)

    def add_mine(self) -> None:
        self._mine_count += 1

    def get_mine_count(self) -> int:
        return self._mine_count

    def is_mine(self) -> bool:
        return self._mine

    def set_mine(self) -> None:
        self._mine = True

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
