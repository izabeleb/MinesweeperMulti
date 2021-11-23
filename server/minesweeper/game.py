import datetime

import uuid

from minesweeper.minefield import MineField


class MinesweeperGame:
    def __init__(self, height: int, width: int, mine_count: int):
        self.created_at = datetime.datetime.now()
        self.id = uuid.uuid4()

        self.minefield = MineField(height, width, mine_count)
