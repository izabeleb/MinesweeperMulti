import React from 'react';
import { MinesweeperService } from '../api/api';
import { GameData } from '../api/types';
import { Cell } from './minesweeper/types';
import { MinefieldCommponent } from './minesweeper/minefield';

interface GameProps {
    gameData: GameData,
  
    service: MinesweeperService,
}
  
interface GameState {
    cells?: Cell[][],
    is_flag_mode: boolean,
}

export class GameComponent extends React.Component<GameProps, GameState> {
    service: MinesweeperService;
  
    constructor(props: GameProps) {
        super(props)
  
        this.service = props.service;
      
        this.state = {
            is_flag_mode: false,
        }
    }

    componentDidMount() {
        if (this.state.cells === undefined) {
            this.service.getField(this.props.gameData.id)
                .then(cells => this.setState({cells: cells}));
        }
    }
  
    render() {
        return  <div>{ this.state.cells !== undefined ? <MinefieldCommponent cells={this.state.cells} is_flag_mode={this.state.is_flag_mode} /> : null }</div>
    }
}