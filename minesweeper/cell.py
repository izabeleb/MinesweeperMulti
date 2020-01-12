class Cell:
    """Wrapper class for each cell in a MineField field.

    Args:
        row (int): the row the cell is located int.
        col (in): the column the cell is located in
        is_mine (bool): whether the cell is a mine or not.
        is_flag (bool): whether teh user has marked the cell with a flag or not.
        mine_count (int): the amount of mines surrounding the cell.
        visited (bool): whether the cell has been visited when opening cells or not.
        clicked (bool): whether the the cell has been clicked by the user or not.
    """

    def __init__(self, row: int, col: int, is_mine: bool = False, is_flag: bool = False,
                 mine_count: int = 0, visited: bool = False, clicked: bool = False):
        self.row: int = row
        self.col: int = col
        self.is_mine: bool = is_mine
        self.is_flag: bool = is_flag
        self.mine_count: int = mine_count
        self.visited: bool = visited
        self.clicked: bool = clicked

    def __repr__(self):
        if self.is_mine:
            return '#'
        else:
            return repr(self.mine_count)

    def add_mine(self):
        """Increment the amount of mines surrounding the cell."""
        self.mine_count += 1
