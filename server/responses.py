from minesweeper.minefield import MineField

from typing import NamedTuple

from uuid import UUID


class PostGameResponse(NamedTuple):
    """Response to a crate game request."""
    game_uuid: UUID
    mine_field: MineField


class GetGameIdsResponse(NamedTuple):
    """Response to a field query."""
    game_uuids: list[UUID]


class GetGameResponse(NamedTuple):
    """Response to a field access request."""
    mine_field: MineField


class PutGameResponse(NamedTuple):
    """Response to a field state update request."""
