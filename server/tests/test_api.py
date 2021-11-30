import app

import unittest

from api.service import MinesweeperService, MemoryStore
from api.requests import *

from minesweeper.game import MinesweeperGame, GameEvent, EventType
from minesweeper.cell import CellStatus

import uuid
from uuid import UUID

import json


def _to_json_dict(obj):
    return json.loads(json.dumps(obj, cls=app.MinesweeperEncoder))


class BaseWrapper:
    class BaseGameTest(unittest.TestCase):
        def setUp(self):
            self._store = MemoryStore()
            self._client = app.create_app(self._store).test_client()
            self._service = MinesweeperService(self._store)


class TestGetGame(BaseWrapper.BaseGameTest):
    def setUp(self):
        super().setUp()

        self._game_0 = MinesweeperGame(4, 4, 0)
        self._game_1 = MinesweeperGame(4, 4, 0)
        self._game_2 = MinesweeperGame(4, 4, 0)
        self._game_3 = MinesweeperGame(4, 4, 0)
        self._game_4 = MinesweeperGame(4, 4, 0)

        self._sorted_games = sorted([
            self._game_0,
            self._game_1,
            self._game_2,
            self._game_3,
            self._game_4
        ],
            key=lambda game: game.created_at)

        self._store.add_game(self._game_0)
        self._store.add_game(self._game_1)
        self._store.add_game(self._game_2)
        self._store.add_game(self._game_3)
        self._store.add_game(self._game_4)

    def test_get_game(self):
        response = self._client.get(f"/game/{self._game_0.id}")

        actual = response.json
        expected = {
            'game': {
                'created_at': self._game_0.created_at.timestamp(),
                'id': str(self._game_0.id),
                'width': self._game_0.width,
                'height': self._game_0.height,
                'mine_count': self._game_0.mine_count,
            }
        }

        self.assertDictEqual(expected, actual)

    def test_get_non_existent_game(self):
        response = self._client.get(f"/game/{uuid.uuid4()}")

        self.assertEqual(404, response.status_code)

    def test_get_page_size_3(self):
        response = self._client.get(f"/games?page=1&size=3")

        self.assertListEqual(_to_json_dict([self._game_0, self._game_1, self._game_2]),
                             response.json["page"]["data"])

        response = self._client.get(f"/games?page=2&size=3")
        self.assertListEqual(_to_json_dict([self._game_3, self._game_4]),
                             response.json["page"]["data"])


class TestPostGame(BaseWrapper.BaseGameTest):
    def test_no_body(self):
        response = self._client.post("/games", data=None)

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
            "mine_count": 0
        })

        response_json = response.json
        game_id = UUID(response_json["id"])

        game = self._store.get_game(game_id)

        if game is None:
            self.fail("game should not be None")

        self.assertEqual(10, game.minefield.rows)
        self.assertEqual(10, game.minefield.cols)
        self.assertEqual(0, game.minefield.mine_count)

    def test_bad_field_dimensions(self):
        response = self._client.post("/games", json={
            "width": 10,
            "height": -1,
            "mine_count": 0
        })

        self.assertEqual(400, response.status_code)


class TestUpdateGame(BaseWrapper.BaseGameTest):
    def setUp(self):
        super().setUp()

        response = self._service.create_game(PostGameRequest(4, 4, 0))

        self._game_id = response.id
        self._game = self._store.get_game(self._game_id)
        self._minefield = self._game.minefield

    def test_update_non_existent_game(self):
        response = self._client.patch(f"/game/{uuid.uuid4()}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Opened,
        })

        self.assertEqual(404, response.status_code)

    def test_open_empty(self):
        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Opened,
        })

        for row in self._minefield.cells:
            for cell in row:
                if cell.status != CellStatus.Opened:
                    self.fail("all cells should be open")

        actual = [event.event_type for event in self._game.events]
        expected = [EventType.GameStart] + [EventType.CellChange] * 16

        self.assertListEqual(expected, actual)

    def test_open_mine(self):
        self._minefield.cells[0][0].is_mine = True

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Opened,
        })

        response = self._service.get_game_events(GetGameEventsRequest(self._game_id))

        actual = [event.event_type for event in response.events]
        expected = [EventType.GameStart, EventType.CellChange, EventType.GameEnd]

        self.assertListEqual(expected, actual)

    def test_update_flagged_cell(self):
        self._minefield.cells[0][0].status = CellStatus.Flagged

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Opened,
        })

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Flagged,
        })

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Closed,
        })

        response = self._service.get_game_events(GetGameEventsRequest(self._game_id))

        actual = [event.event_type for event in response.events]
        expected = [EventType.GameStart, EventType.CellChange]

        self.assertListEqual(expected, actual)

    def test_update_open_cell(self):
        self._minefield.cells[0][0].status = CellStatus.Opened

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Closed,
        })

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Opened,
        })

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Flagged,
        })

        response = self._service.get_game_events(GetGameEventsRequest(self._game_id))

        actual = [event.event_type for event in response.events]
        expected = [EventType.GameStart]

        self.assertListEqual(expected, actual)

    def test_update_closed_cell(self):
        # see TestUpdateGame.test_hist_empty for changing the status of a closed
        # cell to open in a minefield with no mines
        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Flagged,
        })

        response = self._service.get_game_events(GetGameEventsRequest(self._game_id))

        actual = [event.event_type for event in response.events]
        expected = [EventType.GameStart, EventType.CellChange]

        self.assertListEqual(expected, actual)

    def test_open_numbered_cell(self):
        self._minefield.set_mine(1, 1)

        self._client.patch(f"/game/{self._game_id}/field", json={
            "row": 0,
            "col": 0,
            "status": CellStatus.Opened,
        })

        response = self._service.get_game_events(GetGameEventsRequest(self._game_id))

        actual = [event.event_type for event in response.events]
        expected = [EventType.GameStart, EventType.CellChange]

        self.assertListEqual(expected, actual)


class TestGameEvents(BaseWrapper.BaseGameTest):
    def setUp(self):
        super().setUp()

        self._game = MinesweeperGame(4, 4, 0)
        self._events = self._game.events

        self._store.add_game(self._game)

        self._events.append(GameEvent(EventType.GameStart, None))
        self._events.append(GameEvent(EventType.CellChange, CellChange(0, 0, CellStatus.Opened)))
        self._events.append(GameEvent(EventType.GameEnd, None))

        self._start_time = self._events[0].occurred_at
        self._middle_time = self._events[len(self._events) // 2].occurred_at
        self._end_time = self._events[-1].occurred_at

    def test_events_non_existent_game(self):
        response = self._client.get(f"/game/{uuid.uuid4()}/events")

        self.assertEqual(404, response.status_code)

    def test_events_no_since(self):
        response = self._client.get(f"/game/{self._game.id}/events")

        actual = response.json["events"]
        expected = _to_json_dict(self._events)

        self.assertListEqual(expected, actual)

    def test_events_since_start(self):
        response = self._client.get(f"/game/{self._game.id}/events?since={self._start_time.timestamp()}")

        actual = response.json["events"]
        expected = _to_json_dict(self._events[1:])

        self.assertListEqual(expected, actual)

    def test_events_since_middle(self):
        response = self._client.get(f"/game/{self._game.id}/events?since={self._middle_time.timestamp()}")

        actual = response.json["events"]
        expected = _to_json_dict(self._events[-1:])

        self.assertListEqual(expected, actual)

    def test_events_since_end(self):
        response = self._client.get(f"/game/{self._game.id}/events?since={self._end_time.timestamp()}")

        actual = response.json["events"]
        expected = _to_json_dict([])

        self.assertListEqual(expected, actual)


class TestGameField(BaseWrapper.BaseGameTest):
    def setUp(self):
        super().setUp()

        self._game = MinesweeperGame(4, 4, 4)
        self._minefield = self._game.minefield
        self._cells = self._minefield.cells

        self._store.add_game(self._game)

    def test_field_non_existent_game(self):
        response = self._client.get(f"/game/{uuid.uuid4()}/field")

        self.assertEqual(404, response.status_code)

    def test_field(self):
        response = self._client.get(f"/game/{self._game.id}/field")

        actual = response.json["cells"]
        expected = _to_json_dict(self._cells)

        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
