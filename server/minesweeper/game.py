from dataclasses import dataclass, field

import enum
from enum import Enum

import datetime

import uuid

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


# todo: add events
@dataclass
class MinesweeperGame:
    height: int
    width: int
    mine_count: int

    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
                                          init=False)
    id: datetime.datetime = field(default_factory=uuid.uuid4, init=False)

    def __post_init__(self):
        # since self.minefield is not initialized as a dataclass Field it will
        # not be included in the serialized json for this class
        self.minefield = MineField(self.height, self.width, self.mine_count)
        self.events: list[GameEvent] = list()
