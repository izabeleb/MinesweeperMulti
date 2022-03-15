from dataclasses import dataclass, field

import enum
from enum import Enum

import datetime

import uuid
from uuid import UUID

from minesweeper.cell import CellStatus, CellChange
from minesweeper.minefield import MineField

from typing import Any


@dataclass
class GameLossData:
    closed_mines: list[tuple[int, int]]


@enum.unique
class EventType(str, Enum):
    CellChange = "cell_change"
    GameStart = "game_start"
    GameWin = "game_win"
    GameLoss = "game_loss"


@dataclass
class GameEvent:
    occurred_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
                                           init=False)
    event_type: EventType

    # the event type should be json serializable by the flask JSONEncoder:
    #   https://github.com/pallets/flask/blob/7620cb70dbcbf71bca651e6f2eef3cbb05999272/src/flask/json/__init__.py#L19
    event: Any


@dataclass
class MinesweeperGame:
    height: int
    width: int
    mine_count: int

    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
                                          init=False)
    id: UUID = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        # since self.minefield is not initialized as a dataclass Field it will
        # not be included in the serialized json for this class
        self.minefield = MineField(self.height, self.width, self.mine_count)
        self.events: list[GameEvent] = list()

    def update_cell(self, row: int, col: int, status: CellStatus):
        cell = self.minefield.cells[row][col]

        if status == CellStatus.Flagged:
            if cell.status == CellStatus.Closed:
                cell.status = CellStatus.Flagged
                self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, CellStatus.Flagged)))

        elif status == CellStatus.Opened:
            if cell.status == CellStatus.Closed:
                if cell.is_mine:
                    self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, CellStatus.Opened)))
                    self.events.append(GameEvent(EventType.GameLoss, GameLossData(self.minefield.get_closed_mines())))
                else:
                    if cell.adjacent_mines == 0:
                        for coordinate in self.minefield.get_empty_connected(row, col):
                            empty_cell = self.minefield.cells[coordinate[0]][coordinate[1]]

                            empty_cell.status = CellStatus.Opened
                            self.events.append(GameEvent(EventType.CellChange,
                                                         CellChange(coordinate[0], coordinate[1], CellStatus.Opened)))
                    else:
                        cell.status = CellStatus.Opened
                        self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, CellStatus.Opened)))

                    if self.minefield.is_field_clear():
                        self.events.append(GameEvent(EventType.GameWin, None))

        elif status == CellStatus.Closed:
            if cell.status == CellStatus.Flagged:
                cell.status = CellStatus.Closed
                self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, CellStatus.Closed)))

        else:
            raise ValueError(f"unsupported cell state '{status}'")
