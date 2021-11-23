from dataclasses import dataclass, field

import enum
from enum import Enum


@enum.unique
class CellState(Enum):
    Flag = enum.auto()
    Hit = enum.auto()
    Empty = enum.auto()


@dataclass
class Cell:
    row: int
    col: int

    adjacent_mines: int = field(default=0, init=False)

    is_mine: bool = field(default=False, init=False)

    state: CellState = field(default=CellState.Empty, init=False)

    def __hash__(self):
        return self.get_coordinate().__hash__()

    def get_coordinate(self) -> tuple[int, int]:
        return self.row, self.col

    def to_json(self):
        return {
            "col": self.col,
            "row": self.row,
            "is_mine": self.is_mine,
            "state": self.state
        }
