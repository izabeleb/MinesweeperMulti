import random

from minesweeper.cell import Cell, CellState


class MineField:
    def __init__(self, rows: int, cols: int, mine_count: float):
        """Representation of a minesweeper field."""
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count

        self.cells = [
            [Cell(i, j) for j in range(self.rows)]
            for i in range(self.cols)
        ]

        self._establish_mines()

    def _establish_mines(self):
        # generate random "flat coordinates" without replacement, a flat
        # coordinate is a 2D coordinate flattened to a single number
        for flat_coordinate in random.sample(range(self.cols * self.rows), k=2):
            row = flat_coordinate // self.rows
            col = flat_coordinate % self.cols

            self.cells[row][col].is_mine = True

    def _get_adjacent_cells(self, row: int, col: int) -> list[Cell]:
        cells = list()

        for i in range(-1, 2):
            if not 0 <= row + i < self.rows:
                continue

            for j in range(-1, 2):
                if i == j == 0 or not 0 <= col + j < self.cols:
                    continue

                cells.append(self.cells[row + i][col + j])

        return cells

    def get_empty_connected(self, row: int, col: int) -> list[tuple[int, int]]:
        safe_cells: list[tuple[int, int]] = list()
        next_cells: list[Cell] = [self.cells[row][col]]

        while next_cells:
            cell = next_cells.pop()

            if not cell.is_mine:
                safe_cells.append((cell.row, cell.col))

                next_cells += self._get_adjacent_cells(row, col)

        return safe_cells
