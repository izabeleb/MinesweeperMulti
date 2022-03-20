import { Coordinate } from "../../api/types";

/**
 * Enum specifying the state of a cell.
 */
export enum CellStatus {
    Flagged = "flagged",
    Opened = "opened",
    Closed = "closed",
}

export interface Cell {
    coordinate: Coordinate
    adjacentMines: number,
    isMine: boolean,
    status: CellStatus,
}