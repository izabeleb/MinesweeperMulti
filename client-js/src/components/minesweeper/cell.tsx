import React from 'react';

import { Button } from '@react95/core';
import { Confcp109, Winmine1 } from '@react95/icons';

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
                icon = <Confcp109 variant="16x16_4" />

                break;
            case CellStatus.Opened:
                if (isMine) {
                    icon = <Winmine1 variant="16x16_4" />
                }

                break;
            case CellStatus.Closed:
                break;
        }

        return <Button style={{height: 'parent'}}>
            {icon}
        </Button>
    }
}

