class Cell:
    """Wrapper class for each cell in a MineField field."""

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.mine_count = 0
        self.mine: bool = False
        self.flag: bool = False

    def __repr__(self):
        if self.mine:
            return '#'
        else:
            return repr(self.mine_count)

    def add_mine(self) -> None:
        self.mine_count += 1

    def get_mine_count(self) -> int:
        return self.mine_count

    def is_mine(self) -> bool:
        return self.mine

    def set_mine(self) -> None:
        self.mine = True

    def is_flag(self) -> None:
        return self.flag

    def set_flag(self, flag) -> None:
        self.flag = flag
