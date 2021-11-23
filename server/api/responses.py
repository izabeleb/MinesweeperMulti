from minesweeper.game import MinesweeperGame

from typing import NamedTuple

from uuid import UUID


class PostGameResponse(NamedTuple):
    """Response to a crate game request."""
    game_url: str


class GetGamesResponse(NamedTuple):
    """Response to a field query."""
    games: list[MinesweeperGame]


class GetGameResponse(NamedTuple):
    """Response to a field access request."""
    game: MinesweeperGame


class UpdateGameFieldResponse(NamedTuple):
    """Response to a field state update request."""
