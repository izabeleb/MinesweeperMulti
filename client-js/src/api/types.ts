import { CellStatus } from "../components/minesweeper/types";

export interface GameData {
    id: string, // todo: might be better to use a concrete UUID type here
    height: number,
    width: number,
    mineCount: number,
    createdAt: Date,
}

export enum EventType {
    GameStart = "game_start",
    CellChange = "cell_change",
    GameWin = "game_win",
    GameLoss = "game_loss",
}

export interface CellChange {
    row: number,
    col: number,
    status: CellStatus,
}

export interface GameLossData {
    closedMines: number[][] // todo: we probably want to make a "Coordiante" type here (will need to match on the backend)
}

/**
 * Simple abstraction around a number as the milliseconds since the epoch.
 */
export type Epoch = number;


export interface GameEvent {
    occurredAt: Epoch,
    eventType: EventType,
    event: CellChange | { }
}

/**
 * An abstraction around a page of data specifying the page number, the maximum
 * size of the data payload, and the payload.
 */
 export interface IPage<T> {
    page: number,
    size: number,
    data: T[],
}

