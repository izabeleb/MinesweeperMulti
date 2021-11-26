import React from 'react';
import ReactDOM from 'react-dom';
import { CellCommponent, Cell, CellStatus } from './components/minesweeper/cell';
import reportWebVitals from './reportWebVitals';

var root_cell: Cell = {
  row: 0,
  col: 0,
  adjacentMines: 0,
  isMine: true,
  status: CellStatus.Opened,
} as Cell;

ReactDOM.render(
  <React.StrictMode>
    <CellCommponent cell={root_cell} />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
