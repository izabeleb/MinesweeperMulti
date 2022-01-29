import React from 'react';
import _ from 'lodash';
import { MinesweeperService } from '../api/api';
import { CellChange, Epoch, EventType, GameData, GameEvent } from '../api/types';
import { Cell, CellStatus } from './minesweeper/types';
import { MinefieldCommponent } from './minesweeper/minefield';
//import { GamebarComponent } from './minesweeper/gamebar';

interface GameProps {
    gameData: GameData,

    service: MinesweeperService,
}

interface GameState {
    cells?: Cell[][],

    isFlagMode: boolean,

    isGameOver: boolean,
}

/**
 * The interval in milliseconds to poll the backend server.
 */
const POLL_INTERVAL: number = 200;

export class GameComponent extends React.Component<GameProps, GameState> {
    private intervalId?: NodeJS.Timeout;
    private lastEventOccurence?: Epoch;

    constructor(props: GameProps) {
        super(props);

        this.state = {
            isFlagMode: false,
            isGameOver: false, // todo: verify with rest call
        }
    }

    updateCell = (row: number, col: number, status: CellStatus) => {
        this.props.service.patchField(this.props.gameData.id, row, col, status);
    }

    handleNewEvents(events: GameEvent[]) {
        this.setState(previousState => {
            let cells = previousState.cells;
            let is_game_over: boolean = previousState.isGameOver;

            if (cells !== undefined) {
                cells = _.cloneDeep(cells);

                events.forEach(event => {
                    switch (event.eventType) {
                        case EventType.GameStart:
                            // do nothing...
                            break;
                        case EventType.CellChange:
                            let change: CellChange = event.event as CellChange;
                            cells![change.row][change.col].status = change.status;

                            break;
                        case EventType.GameEnd:
                            is_game_over = true;
                            break;
                    }
                });

                if (events.length > 0) {
                    this.lastEventOccurence = events[events.length - 1].occurredAt;
                }
            }

            return { cells: cells, isGameOver: is_game_over }
        });
    }

    componentDidMount() {
        if (this.state.cells === undefined) {
            this.props.service.getField(this.props.gameData.id)
                .then(cells => this.setState({cells: cells}));
        }

        this.intervalId = setInterval(() => {
            this.props.service.getGameEvents(this.props.gameData.id, this.lastEventOccurence).then(events => {
                if (events.length !== 0) {
                    this.lastEventOccurence = events[events.length - 1].occurredAt;
                    this.handleNewEvents(events);
                }
            })
        }, POLL_INTERVAL);
    }

    componentWillUnmount() {
        if (this.intervalId !== undefined) {
            clearInterval(this.intervalId);
        }
    }

    render() {
        return  <div>

          <div className="minefield-scroll">
          { this.state.cells !== undefined ? <MinefieldCommponent cellUpdater={this.updateCell} cells={this.state.cells} isFlagMode={this.state.isFlagMode} /> : null }
          </div>
        </div>
    }
}
