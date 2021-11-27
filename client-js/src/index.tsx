import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import { MinesweeperService, GameData } from './api/api'
import { GameComponent } from './components/game';

import '98.css';
import './components/minesweeper/cell.css';
import './components/minesweeper/minefield.css';

interface IProps {
    service: MinesweeperService,
}

interface IState {
    game?: GameData,
}

/**
 * Basic wrapper componen around the game component which fetches the game data.
 */
class WrapperComponent extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);

        this.state = {
        
        };
    }

    componentDidMount() {
        this.props.service.createGame(4, 4, 4)
        .then(id => this.props.service.getGame(id)
            .then(data => this.setState({game: data})));
  }

    render() {
        return <div>{ this.state.game !== undefined ? <GameComponent service={this.props.service} gameData={this.state.game} /> : 'no game data available'}</div>
      }
}

let service = new MinesweeperService("localhost:5000");

ReactDOM.render(
  <React.StrictMode>
    <WrapperComponent service={service}/>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
