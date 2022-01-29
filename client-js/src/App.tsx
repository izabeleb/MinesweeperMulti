import React from 'react';
import { Link } from 'react-router-dom';
import { MinesweeperService } from './api/api';

interface IProps {
    service: MinesweeperService,
}

interface IState {
}

/**
 * Basic wrapper component around the game component which fetches the game data.
 */
export class App extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);

        this.state = {
        };
    }

    render() {
        return (
          <div className="menu">
          <p className="menu-header-no-hover">MultiMine</p>
          <Link className="menu-item" to="/newgame">New Game</Link>
          <br/>
          <Link className="menu-item" to="/games">Current Games</Link>
          </div>
        )
    }
}
