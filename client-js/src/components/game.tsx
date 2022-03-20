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

    isGameWon: boolean,
}

/**
 * The interval in milliseconds to poll the backend server.
 */
const POLL_INTERVAL: number = 200;

export class GameComponent extends React.Component<GameProps, GameState> {
    private getEventsInterval?: NodeJS.Timeout;
    private lastEventOccurence?: Epoch;

    constructor(props: GameProps) {
        super(props);

        this.state = {
            isFlagMode: false,
            isGameOver: false,
            isGameWon: false,
        }
    }

    updateCell = (row: number, col: number, status: CellStatus) => {
        this.props.service.patchField(this.props.gameData.id, row, col, status);
    }

    handleNewEvents(events: GameEvent[]) {
        this.setState(previousState => {
            let { cells, isGameOver, isGameWon } = previousState;

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
                        case EventType.GameWin:
                            isGameOver = true;
                            isGameWon = true;

                            break;
                        case EventType.GameLoss:
                            isGameOver = true;
                            isGameWon = false;

                            break;
                    }
                });

                if (events.length > 0) {
                    this.lastEventOccurence = events[events.length - 1].occurredAt;
                }
            }

            if (isGameOver && this.getEventsInterval) {
                clearInterval(this.getEventsInterval);
                this.getEventsInterval = undefined;
            }

            return { cells: cells, isGameOver: isGameOver, isGameWon: isGameWon }
        });
    }

    componentDidMount() {
        if (this.state.cells === undefined) {
            this.props.service.getField(this.props.gameData.id)
                .then(cells => this.setState({cells: cells}));
        }

        this.getEventsInterval = setInterval(() => {
            this.props.service.getGameEvents(this.props.gameData.id, this.lastEventOccurence).then(events => {
                if (events.length !== 0) {
                    this.lastEventOccurence = events[events.length - 1].occurredAt;
                    this.handleNewEvents(events);
                }
            })
        }, POLL_INTERVAL);
    }

    componentWillUnmount() {
        if (this.getEventsInterval) {
            clearInterval(this.getEventsInterval);
        }
    }

    render() {
        let { isGameOver, isGameWon } = this.state;
        let header = null;

        if (isGameOver) {
            if (isGameWon) {
                header = <div>You Won :)</div>
            } else {
                header = <div>You Lost :(</div>
            }
        }

        return <div>
            <div className="minefield-scroll">
                {header}

                { this.state.cells !== undefined ? <MinefieldCommponent cellUpdater={this.updateCell} cells={this.state.cells} isFlagMode={this.state.isFlagMode} isActive={! isGameOver} /> : null }
          </div>
        </div>
    }
}
