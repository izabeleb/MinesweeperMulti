import React from 'react';
import { GameData, IPage, MinesweeperService } from '../api/api';
import { Cell, CellStatus } from './minesweeper/cell';
import { MinefieldCommponent } from './minesweeper/minefield';

interface GameProps {
    gameData: GameData,
  
    service: MinesweeperService,
}
  
interface GameState {
    cells?: Cell[][]
}

export class GameComponent extends React.Component<GameProps, GameState> {
    service: MinesweeperService;
  
    constructor(props: GameProps) {
        super(props)
  
        this.service = props.service;
      
        this.state = {

        }
    }

    componentDidMount() {
        this.service.getField(this.props.gameData.id)
            .then(cells => this.setState({cells: cells}));
    }
  
    render() {
        return  <div>{ this.state.cells !== undefined ? <MinefieldCommponent cells={this.state.cells} /> : null }</div>
    }
}