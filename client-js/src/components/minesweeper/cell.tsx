import React from 'react';

export enum CellStatus {
    Flagged = "flagged",
    Opened = "opened",
    Closed = "closed",
}

export interface Cell {
    row: number,
    col: number,
    adjacentMines: number,
    isMine: boolean,
    status: CellStatus,
}

interface CellProps {
    cell: Cell,
}

interface CellState { }

export class CellCommponent extends React.Component<CellProps, CellState> {

    constructor(props: CellProps) {
        super(props)

        this.state = {
            status: CellStatus.Opened
        }
    }

    render() {
        let {isMine, status} = this.props.cell;

        let icon = null;

        switch (status) {
            case CellStatus.Flagged:
                icon = <div>flagged</div>

                break;
            case CellStatus.Opened:
                icon = <div>opened</div>

                break;
            case CellStatus.Closed:
                icon = <div>closed</div>
                break;
        }

        return icon
    }
}

