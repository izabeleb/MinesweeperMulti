import itertools

import app

import unittest

from api.service import MemoryStore

from minesweeper.game import MinesweeperGame
from minesweeper.cell import CellState

import uuid
from uuid import UUID


class TestGetGame(unittest.TestCase):
    def setUp(self):
        self._game_0 = MinesweeperGame(10, 10, 10)
        self._game_1 = MinesweeperGame(10, 10, 10)
        self._game_2 = MinesweeperGame(10, 10, 10)
        self._game_3 = MinesweeperGame(10, 10, 10)
        self._game_4 = MinesweeperGame(10, 10, 10)

        self._sorted_games = sorted([
                                        self._game_0,
                                        self._game_1,
                                        self._game_2,
                                        self._game_3,
                                        self._game_4
                                    ],
                                    key=lambda game: game.created_at)

        self._store = MemoryStore()
        self._store.add_game(self._game_0)
        self._store.add_game(self._game_1)
        self._store.add_game(self._game_2)
        self._store.add_game(self._game_3)
        self._store.add_game(self._game_4)

        self._client = app.create_app(self._store).test_client()

    def test_get_game(self):
        response = self._client.get(f"/game/{self._game_0.id}")

        actual = response.json
        expected = {
            'created_at': self._game_0.created_at.timestamp(),
            'url': f'/game/{self._game_0.id}'
        }

        self.assertEqual(expected, actual)

    def test_get_non_existent_game(self):
        response = self._client.get(f"/game/{uuid.uuid4()}")

        self.assertEqual(404, response.status_code)

    def test_get_page_size_3(self):
        response = self._client.get(f"/games?page=1&size=3")
        self.assertListEqual(response.json["data"], [i.to_json() for i in [self._game_0, self._game_1, self._game_2]])

        response = self._client.get(f"/games?page=2&size=3")
        self.assertListEqual(response.json["data"], [i.to_json() for i in [self._game_3, self._game_4]])


class TestPutGame(unittest.TestCase):
    def setUp(self):
        self._store = MemoryStore()

        self._client = app.create_app(self._store).test_client()

    def test_no_body(self):
        response = self._client.post("/games", data={})

        self.assertEqual(400, response.status_code)

    def test_unrecognized_field(self):
        response = self._client.post("/games", data={
            "unrecognized_field": "unrecognized_value"
        })

        self.assertEqual(400, response.status_code)

    def test_basic_field(self):
        response = self._client.post("/games", json={
            "width": 10,
            "height": 10,
            "mine_count": 10
        })

        response_json = response.json
        game_url = response_json["game_url"]
        game_id = UUID(game_url.split("/")[-1])

        game = self._store.get_game(game_id)

        self.assertEqual(10, game.minefield.rows)
        self.assertEqual(10, game.minefield.cols)
        self.assertEqual(10, game.minefield.mine_count)

    def test_bad_field_dimensions(self):
        response = self._client.post("/games", json={
            "width": 10,
            "height": -1,
            "mine_count": 10
        })

        self.assertEqual(400, response.status_code)


class TestUpdateGame(unittest.TestCase):
    def setUp(self):
        self._store = MemoryStore()

        self._client = app.create_app(self._store).test_client()

        response = self._client.post("/games", json={
            "width": 4,
            "height": 4,
            "mine_count": 0
        })

        response_json = response.json

        self._game_url = response_json["game_url"]
        self._game_id = UUID(self._game_url.split("/")[-1])
        self._game = self._store.get_game(self._game_id)
        self._minefield = self._game.minefield

    def test_update_non_existent_game(self):
        response = self._client.patch(f"/game/{uuid.uuid4()}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Open,
            }
        })

        self.assertEqual(404, response.status_code)

    def test_hit_empty(self):
        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Open,
            }
        })

        expected = sorted(list(itertools.chain(*[
            [{"col": j, "row": i, "state": "opened"} for j in range(self._minefield.cols)]
            for i in range(self._minefield.rows)
        ])), key=lambda i: (i["row"], i["col"]))
        actual = sorted(response.json["cell_changes"], key=lambda i: (i["row"], i["col"]))

        self.assertListEqual(expected, actual)

        for row in self._minefield.cells:
            for cell in row:
                if cell.state != CellState.Open:
                    self.fail("all cells should be hit")

    def test_hit_mine(self):
        self._minefield.cells[0][0].is_mine = True

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Open,
            }
        })

        self.assertTrue(response.json["is_mine_hit"])

    def test_update_flagged_cell(self):
        self._minefield.cells[0][0].state = CellState.Flag

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Open,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": []}, response.json)

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Flag,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": []}, response.json)

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Closed,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": [{"row": 0, "col": 0, "state": "closed"}]}, response.json)

    def test_update_open_cell(self):
        self._minefield.cells[0][0].state = CellState.Open

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Closed,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": []}, response.json)

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Open,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": []}, response.json)

        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Flag,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": []}, response.json)

    def test_update_closed_cell(self):
        # see testUpdateGame.test_hist_empty for changing the state of a closed
        # cell to open in a minefield with no mines
        response = self._client.patch(f"/game/{self._game_id}/field", json={
            "cell_change": {
                "row": 0,
                "col": 0,
                "state": CellState.Flag,
            }
        })

        self.assertDictEqual({"is_mine_hit": False, "cell_changes": [{"col": 0, "row": 0, "state": "flag"}]}, response.json)
