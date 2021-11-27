export interface GameData {
    id: string, // todo: might be better to use a concrete UUID type here
    height: number,
    width: number,
    mineCount: number,
    createdAt: Date,
}

export enum EventType {
    CellChange = "cell_change",
    GameStart = "game_start",
    GameEnd = "game_end",
}

export interface GameEvent {
    occurredAt: Date,
    eventType: EventType,
    event: any
}