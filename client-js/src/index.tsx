import ReactDOM from 'react-dom';
import { MinesweeperService } from './api/api'
import { App } from './App';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import '98.css';
import './components/minesweeper/cell.css';
import './components/minesweeper/minefield.css';
import { GamesRoute } from './routes/games';

let service = new MinesweeperService("localhost:5000");

service.createGame(10, 10, 4);
service.createGame(10, 10, 10);

async function sleep(ms: number) {
    await new Promise(resolve => setTimeout(resolve, ms));
}

sleep(2000);

const rootElement  = document.getElementById("root");

// todo: add routes
ReactDOM.render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<App service={service}/>} />
            <Route path="/games" element={<GamesRoute service={service} />} />
            {/* <Route path="game/:id" /> */}
        </Routes>
    </BrowserRouter>,
    rootElement
);
