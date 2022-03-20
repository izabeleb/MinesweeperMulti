from dataclasses import dataclass, field

import enum
from enum import Enum


@enum.unique
class CellStatus(str, Enum):
    Flagged = "flagged"
    Opened = "opened"
    Closed = "closed"


@dataclass
class CellChange:
    row: int
    col: int
    status: CellStatus


@dataclass
class Cell:
    row: int
    col: int

    adjacent_mines: int = field(default=0, init=False)

    is_mine: bool = field(default=False, init=False)

    status: CellStatus = field(default=CellStatus.Closed, init=False)

    def __hash__(self):
        return self.get_coordinate().__hash__()

    def get_coordinate(self) -> tuple[int, int]:
        return self.row, self.col
