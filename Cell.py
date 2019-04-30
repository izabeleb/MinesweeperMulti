class Cell:
    """Wrapper class for each cell in a MineField field."""

    # Provide easy type clasifuers
    EMPTY:    int = 0
    MINE:     int = 1
    NONEMPTY: int = 2

    def __init__(self, x: int, y:int):
        self.x: int = x
        self.y: int = y
        self.bomb_count = 0
        self.cell_type = Cell.EMPTY

    def __repr__(self):
        return repr(self.cell_type)

    def add_mine(self):
        self.bomb_count += 1

    def set_type(self, cell_type: int):
        self.cell_type = cell_type

    def get_type(self):
        return self.cell_type
