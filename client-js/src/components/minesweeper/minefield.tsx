import React from 'react';
import { Cell, CellStatus } from './cell';

interface MinefieldProps {
    rows: number,
    cols: number,
}

interface MinefieldState {
    cells: Cell[][]
}

export default class MinefieldCommponent extends React.Component<MinefieldProps, MinefieldState> {
    constructor(props: MinefieldProps) {
        super(props)

        let cells: Cell[][] = [];

        for (let i = 0; i < props.rows; i++) {
            cells[i] = [];

            for (let j = 0; j < props.cols; j++) {
                cells[i][j] = {
                    row: i,
                    col: j,
                    adjacentMines: 0,
                    isMine: false,
                    status: CellStatus.Opened,
                    // status: CellStatus.Closed,
                } as Cell;
            }
        }

        this.state = {
            cells: cells,
        }
    }
    
    render() {
        return <div>minefield</div>
    }
}