from dataclasses import dataclass, field

import enum
from enum import Enum

import datetime

import uuid
from uuid import UUID

from minesweeper.cell import CellStatus, CellChange
from minesweeper.minefield import MineField

from typing import Any


@enum.unique
class EventType(str, Enum):
    CellChange = "cell_change"
    GameStart = "game_start"
    GameEnd = "GameEnd"


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

    def update_cell(self, row: int, col: int, state: CellStatus) -> bool:
        cell = self.minefield.cells[row][col]
        is_mine_hit = False

        if state == CellStatus.Flagged:
            if cell.state == CellStatus.Closed:
                cell.state = state

                self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, state)))
        elif state == CellStatus.Opened:
            if cell.state == CellStatus.Closed:
                if cell.is_mine:
                    is_mine_hit = True

                    self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, state)))
                    self.events.append(GameEvent(EventType.GameEnd, {}))

                elif cell.state != CellStatus.Opened:
                    for coordinate in self.minefield.get_empty_connected(row, col):
                        empty_cell = self.minefield.cells[coordinate[0]][coordinate[1]]
                        empty_cell.state = CellStatus.Opened

                        self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, state)))
        elif state == CellStatus.Closed:
            if cell.state == CellStatus.Flagged:
                cell.state = state

                self.events.append(GameEvent(EventType.CellChange, CellChange(row, col, state)))
        else:
            raise ValueError(f"unsupported cell state '{state}'")

        return is_mine_hit
