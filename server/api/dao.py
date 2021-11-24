import dataclasses
from dataclasses import dataclass

from uuid import UUID

from minesweeper.game import MinesweeperGame
from minesweeper.cell import CellState

from typing import Any, Optional

from threading import Semaphore


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
    """An in memory storage for minesweeper games.

    This class manages an internal semaphore for each minesweeper game. If you
    need to modify a value instead of simply accessing it, use one of the
    mutator methods to ensure that the integrity of the data is preserved.
    """

    def __init__(self):
        self.games: dict[UUID: (Semaphore, MinesweeperGame)] = dict()

    def add_game(self, game: MinesweeperGame):
        self.games[game.id] = Semaphore(), game

    def get_game(self, game_id: UUID) -> Optional[MinesweeperGame]:
        try:
            _, game = self.games[game_id]

            return game
        except KeyError:
            return None

    def get_page(self, page: int, size: int) -> Page:
        games = sorted(map(lambda t: t[1], self.games.values()),
                       key=lambda game: game.created_at)[size * (page - 1): size * (page - 1) + size]

        return Page(page, size, games)

    def set_cell_state(self, game_id: UUID, row: int, col: int, state: CellState):
        if game_id not in self.games:
            return None

        semaphore, game = self.games[game_id]

        with semaphore:
            return game.update_cell(row, col, state)
