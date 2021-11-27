import { Cell } from "../components/minesweeper/cell";
import _ from 'lodash';

export interface GameData {
    id: string, // todo: might be better to use a concrete UUID type here
    height: number,
    width: number,
    mineCount: number,
    createdAt: Date,
}

function postGameEndpoint(base_url: string): string {
    return `http://${base_url}/games`
}

function getGamesEndpoint(base_url: string, page: number, size: number): string {
    return `http://${base_url}/games?page=${page}&size=${size}`
}

function getGameEndpoint(base_url: string, id: string): string {
    return `http://${base_url}/game/${id}`
}

function getGameFieldEndpoint(base_url: string, id: string): string {
    return `http://${base_url}/game/${id}/field`
}

export interface IPage<T> {
    page: number,
    size: number,
    data: T[],
}

export class MinesweeperService {
    base_url: string;

    constructor(base_url: string) {
        this.base_url = base_url;
    }

    private _snakeToCamelObject(data: any) {
        return _.mapKeys(data, (v, k) => _.camelCase(k))
    }

    async createGame(width: number, height: number, mineCount: number): Promise<string> {
        const response = await fetch(postGameEndpoint(this.base_url), {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
              },
            body: JSON.stringify({
                "width": width,
                "height": height,
                "mine_count": mineCount,
            })
        });
        const json = await response.json();
        const id = json.id;

        return id
    }

    async getGames(page: number = 1, size: number = 10): Promise<IPage<GameData>> {
        const response = await fetch(getGamesEndpoint(this.base_url, page, size));
        const json = await response.json();

        return this._snakeToCamelObject(json['page']) as IPage<GameData>
    }

    async getGame(id: string): Promise<GameData> {
        const response = await fetch(getGameEndpoint(this.base_url, id));
        const json = await response.json();

        return this._snakeToCamelObject(json["game"]) as GameData;
    }

    async getField(id: string): Promise<Cell[][]> {
        const response = await fetch(getGameFieldEndpoint(this.base_url, id));
        const json = await response.json();

        const cells: Cell[][] = json['cells']
            .map((row: Cell[]) => row.map((cell: Cell) => this._snakeToCamelObject(cell)));

        return cells;
    }
}