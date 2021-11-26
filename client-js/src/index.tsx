import React from 'react';
import ReactDOM from 'react-dom';
import { Cell, CellStatus } from './components/minesweeper/cell';
import { MinefieldCommponent } from './components/minesweeper/minefield';
import reportWebVitals from './reportWebVitals';

let rows = 4;
let cols = rows;

let cells: Cell[][] = [];

for (let i: number = 0; i < rows; i++) {
  cells[i] = [];

  for (let j = 0; j < cols; j++) {
    cells[i][j] = {
            row: 0,
            col: 0,
            adjacentMines: 0,
            isMine: false,
            status: CellStatus.Opened,
        } as Cell;
  }
}

cells[0][0].isMine = true;
cells[0][1].status = CellStatus.Flagged;

ReactDOM.render(
  <React.StrictMode>
    <MinefieldCommponent cells={cells}/>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
