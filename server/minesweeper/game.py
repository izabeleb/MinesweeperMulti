import dataclasses
from dataclasses import dataclass, field

import datetime

import uuid

from minesweeper.minefield import MineField


# todo: add events
@dataclass
class MinesweeperGame:
    height: int
    width: int
    mine_count: int

    created_at: datetime.datetime = field(default_factory=datetime.datetime.now, init=False)
    id: datetime.datetime = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        # since self.minefield is not initialized as a dataclass Field it will
        # not be included in the serialized json for this class
        self.minefield = MineField(self.height, self.width, self.mine_count)
