from dataclasses import dataclass, field

import enum
from enum import Enum


# todo: hit -> open -> safe && empty -> close -> unknown ?
@enum.unique
class CellState(str, Enum):
    Flag = "flag"
    Open = "opened"
    Closed = "closed"

    def to_json(self):
        return self


@dataclass
class CellChange:
    row: int
    col: int
    state: CellState

    def to_json(self):
        return {
            "row": self.row,
            "col": self.col,
            "state": self.state
        }


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

    def to_json(self):
        return {
            "col": self.col,
            "row": self.row,
            "is_mine": self.is_mine,
            "state": self.state
        }
