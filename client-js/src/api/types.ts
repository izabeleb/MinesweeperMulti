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
    GameEnd = "game_end",
}

export interface CellChange {
    row: number,
    col: number,
    status: CellStatus,
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