from dataclasses import dataclass, field

import enum
from enum import Enum

from typing import Any


@dataclass
class Coordinate:
    """A basic wrapper around a coordinate on a 2-d plane."""
    row: int
    col: int

    def __hash__(self):
        return hash((self.row, self.col))

    def __lt__(self, other: Any):
        if not isinstance(other, Coordinate):
            raise TypeError(f"'<' not supported between instances of 'Coordinate' and '{type(other)}'")

        return (self.row, self.col) < (other.row, other.col)


@enum.unique
class CellStatus(str, Enum):
    Flagged = "flagged"
    Opened = "opened"
    Closed = "closed"


@dataclass
class CellChange:
    coordinate: Coordinate
    status: CellStatus


@dataclass
class Cell:
    coordinate: Coordinate
    adjacent_mines: int = field(default=0, init=False)

    is_mine: bool = field(default=False, init=False)

    status: CellStatus = field(default=CellStatus.Closed, init=False)

    def __hash__(self):
        return hash(self.coordinate)
