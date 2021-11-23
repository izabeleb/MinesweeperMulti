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