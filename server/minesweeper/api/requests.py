from dataclasses import dataclass, field

import datetime

from uuid import UUID

from minesweeper.cell import CellChange

from typing import Optional


@dataclass(frozen=True)
class PostGameRequest:
    """Request to create a new mine sweeper game."""
    width: int = 10
    height: int = 10
    mine_count: int = 10


@dataclass(frozen=True)
class GetPageRequest:
    """Request for a page of a certain resource."""
    page: int
    size: int


@dataclass(frozen=True)
class GetGameRequest:
    """Request for a specific game."""
    id: UUID


@dataclass(frozen=True)
class UpdateGameFieldRequest:
    """Request to update the state of the game field."""
    id: UUID
    cell_change: CellChange


@dataclass(frozen=True)
class GetGameEventsRequest:
    """Request for a game's events."""
    id: UUID
    since: Optional[datetime.datetime] = field(default=None)


@dataclass(frozen=True)
class GetGameFieldRequest:
    """Request for a game's field cells."""
    id: UUID
