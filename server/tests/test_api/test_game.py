import app

import unittest

from api.service import MemoryStore

from minesweeper.game import MinesweeperGame


class TestGetGame(unittest.TestCase):
    def setUp(self):
        self._store = MemoryStore()
        self._init_game = MinesweeperGame(10, 10, 10)
        self._store.add_game(self._init_game)

    def test_get_game(self):
        client = app.create_app(self._store).test_client()
        response = client.get(f"/game/{self._init_game.id}")

        actual = response.json
        expected = {
            'created_at': self._init_game.created_at.timestamp(),
            'url': f'/game/{self._init_game.id}'
        }

        self.assertEqual(expected, actual)
