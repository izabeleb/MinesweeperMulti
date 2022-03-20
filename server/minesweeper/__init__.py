import minesweeper.api
import minesweeper.minefield
import minesweeper.cell

import datetime

from typing import Any

import flask


class MinesweeperEncoder(flask.json.JSONEncoder):
    """A json encoder to use when converting api request and response data to josn."""
    def default(self, obj: Any):
        if isinstance(obj, datetime.datetime):
            return obj.timestamp()

        return super().default(obj)

