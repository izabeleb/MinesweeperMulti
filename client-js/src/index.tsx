import ReactDOM from 'react-dom';
import { MinesweeperService } from './api/api'
import { App } from './App';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import '98.css';
import './components/minesweeper/cell.css';
import './components/minesweeper/minefield.css';
import { GamesRoute } from './routes/games';
import { GameRoute } from './routes/game';
import { NewgameRoute } from './routes/newgame';

let service = new MinesweeperService("localhost:5000");

const rootElement  = document.getElementById("root");

ReactDOM.render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<App service={service}/>} />
            <Route path="/games" element={<GamesRoute service={service} />} />
            <Route path="/game/:id" element={<GameRoute service={service} />} />
            <Route path="/newgame" element={<NewgameRoute service={service} />} />
        </Routes>
    </BrowserRouter>,
    rootElement
);
