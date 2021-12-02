import React from 'react';
import { Link } from 'react-router-dom';
import { MinesweeperService } from './api/api';
import { GameData } from './api/types';
import { GameComponent } from './components/game';

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
        return <Link to="/games">Games</Link>
    }
}