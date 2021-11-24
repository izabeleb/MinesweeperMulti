import dataclasses
from dataclasses import dataclass

from uuid import UUID

from minesweeper.game import MinesweeperGame

from typing import Any, Optional


@dataclass
class Page:
    """A single page of query results.
    """
    page: int

    size: int

    # all elements of the the page data should be of the same type and should
    # be json serializable by the flask JSONEncoder:
    #   https://github.com/pallets/flask/blob/7620cb70dbcbf71bca651e6f2eef3cbb05999272/src/flask/json/__init__.py#L19
    data: list

    def __post_init__(self):
        for datum in self.data:
            if not dataclasses.is_dataclass(datum):
                raise ValueError("all data values must be dataclasses")


# todo: we probably want some base class so we can implement multiple wrappers around storage mechanisms
class MemoryStore:
    def __init__(self):
        self.games = dict()

    def add_game(self, game: MinesweeperGame):
        self.games[game.id] = game

    def get_game(self, game_id: UUID) -> Optional[MinesweeperGame]:
        try:
            return self.games[game_id]
        except KeyError:
            return None

    def get_page(self, page: int, size: int) -> Page:
        games = sorted(self.games.values(),
                       key=lambda game: game.created_at)[size * (page - 1): size * (page - 1) + size]

        return Page(page, size, games)
