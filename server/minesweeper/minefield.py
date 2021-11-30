import random

from minesweeper.cell import Cell, CellStatus


class MineField:
    def __init__(self, rows: int, cols: int, mine_count: int):
        """Representation of a minesweeper field."""

        if mine_count > rows * cols:
            raise ValueError("mine_count may not be greater than the amount of cells")

        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count

        self.cells = [
            [Cell(i, j) for j in range(self.rows)]
            for i in range(self.cols)
        ]

        self._establish_mines()

    def _establish_mines(self):
        mine_count = 0

        while mine_count < self.mine_count:
            row = random.randrange(self.rows)
            col = random.randrange(self.cols)

            if not self.cells[row][col].is_mine:
                self.set_mine(row, col)

                mine_count += 1

        # todo: above random algorithm has the potential for taking a long time
        #   when generating large mine fields with a high coverage, try finding
        #   random generator with no repeats allowing for O(n) rather than O(∞)
        # for i in range(self.mine_count):
        #     # generate random "flat coordinates" without replacement, a flat
        #     # coordinate is a 2D coordinate flattened to a single number
        #     flat_coordinate = random.sample(range(self.cols * self.rows), k=1)[0]
        #
        #     row = flat_coordinate // self.rows
        #     col = flat_coordinate % self.cols

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
        """Retrieves a list of coordinates of cells which are empty, including the starting coordinate."""
        safe_coordinates: list[tuple[int, int]] = list()
        next_cells: set[Cell] = {self.cells[row][col]}
        visited_cells = set()

        while next_cells:
            cell = next_cells.pop()
            coordinate = cell.get_coordinate()

            if not cell.is_mine:
                safe_coordinates.append(coordinate)

                next_cells |= {adjacent_cell for adjacent_cell in self._get_adjacent_cells(coordinate[0], coordinate[1])
                               if adjacent_cell not in visited_cells}

            visited_cells.add(cell)

        return safe_coordinates

    def set_mine(self, row: int, col: int):
        if not self.cells[row][col].is_mine:
            self.cells[row][col].is_mine = True

            for cell in self._get_adjacent_cells(row, col):
                cell.adjacent_mines += 1
