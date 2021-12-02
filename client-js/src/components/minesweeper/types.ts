/**
 * Enum specifying the state of a cell.
 */
export enum CellStatus {
    Flagged = "flagged",
    Opened = "opened",
    Closed = "closed",
}

export interface Cell {
    row: number,
    col: number,
    adjacentMines: number,
    isMine: boolean,
    status: CellStatus,
}