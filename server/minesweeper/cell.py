from dataclasses import dataclass, field

import enum
from enum import Enum


@enum.unique
class CellState(str, Enum):
    Flag = "flag"
    Open = "opened"
    Closed = "closed"


@dataclass
class CellChange:
    row: int
    col: int
    state: CellState


@dataclass
class Cell:
    row: int
    col: int

    adjacent_mines: int = field(default=0, init=False)

    is_mine: bool = field(default=False, init=False)

    state: CellState = field(default=CellState.Closed, init=False)

    def __hash__(self):
        return self.get_coordinate().__hash__()

    def get_coordinate(self) -> tuple[int, int]:
        return self.row, self.col
