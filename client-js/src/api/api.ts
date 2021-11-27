import { Cell } from "../components/minesweeper/cell";
import _ from 'lodash';

export interface GameData {
    id: string, // todo: might be better to use a concrete UUID type here
    height: number,
    width: number,
    mineCount: number,
    createdAt: Date,
}

/**
 * Retrieve the endpoint for POSTing a new game.
 * 
 * @param base_url the base url for the endopint, typically a domain name.
 * @returns the endpoint to use when creating a new game.
 */
function postGameEndpoint(base_url: string): string {
    return `http://${base_url}/games`
}

/**
 * Retireve the endpoint to use when GETting a list of game pages.
 * 
 * @param base_url the base url for the endopint, typically a domain name.
 * @param page the page number for the quesary (1 based).
 * @param size the amount of reslts you expect to see per page.
 * @returs the endpoint to use when querying for game pages.
 */
function getGamesEndpoint(base_url: string, page: number, size: number): string {
    return `http://${base_url}/games?page=${page}&size=${size}`
}

/**
 * Retrieve the endpoint to use when GETting a specific game.
 * 
 * @param base_url the base url for the endopint, typically a domain name.
 * @param id the id of game to retrieve.
 * @returns the endpoint to use when querying for a specific game.
 */
function getGameEndpoint(base_url: string, id: string): string {
    return `http://${base_url}/game/${id}`
}

/**
 * Retrieve the endpoint to use when GETting a field for a specific game.
 * 
 * @param base_url the base url for the endopint, typically a domain name.
 * @param id the id of game to retrieve.
 * @returns the endpoint to use when querying for a field for a specific game.
 */
function getGameFieldEndpoint(base_url: string, id: string): string {
    return `http://${base_url}/game/${id}/field`
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

/**
 * A service abstraction allowing for a clean interface to the MinesweeperMutli
 * RESTful API.
 * 
 * todo: not complete (missing some api endpoint functionality, mostly dealing
 *       with field updates)
 */
export class MinesweeperService {
    base_url: string;

    constructor(base_url: string) {
        this.base_url = base_url;
    }

    /**
     * Utility to convert a snake cased JSON object to a camel cased JSON object:
     *   { 'is_mine': true } -> { 'isMine': true }
     * 
     * @param data the object to be converted.
     * @returns a JSON object with the key names converted to camel case.
     */
    private _snakeToCamelObject(data: any) {
        return _.mapKeys(data, (v, k) => _.camelCase(k))
    }

    /**
     * Create a new game.
     * 
     * @param width the width of the game field.
     * @param height the height of the game field.
     * @param mineCount the amount fo mines to be populated in the field.
     * @returns a Promise with the string id of the new game.
     */
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

    /**
     * Retrieve a list of games packaged in an IPage.
     * 
     * @param page the pages number to retrieve.
     * @param size the maximum size of the page.
     * @returns a Promise container the specified game data page.
     */
    async getGames(page: number = 1, size: number = 10): Promise<IPage<GameData>> {
        const response = await fetch(getGamesEndpoint(this.base_url, page, size));
        const json = await response.json();

        return this._snakeToCamelObject(json['page']) as IPage<GameData>
    }

    /**
     * Get a specific game by id.
     * 
     * @param id the id of the target game.
     * @returns the game withthe specified id if it exists.
     */
    async getGame(id: string): Promise<GameData> {
        const response = await fetch(getGameEndpoint(this.base_url, id));
        const json = await response.json();

        return this._snakeToCamelObject(json["game"]) as GameData;
    }

    /**
     * Get a specific game field by id.
     * 
     * @param id the of game fo the target field.
     * @returns a list of the cells in a game field.
     */
    async getField(id: string): Promise<Cell[][]> {
        const response = await fetch(getGameFieldEndpoint(this.base_url, id));
        const json = await response.json();

        const cells: Cell[][] = json['cells']
            .map((row: Cell[]) => row.map((cell: Cell) => this._snakeToCamelObject(cell)));

        return cells;
    }
}