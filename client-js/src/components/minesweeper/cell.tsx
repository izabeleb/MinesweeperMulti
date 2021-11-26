import React from 'react';
import { BsFlagFill, BsSquare } from 'react-icons/bs';
import { FaBomb } from 'react-icons/fa';

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
        let iconSize='20px'

        let icon = <BsSquare className="cell_icon" size={iconSize} />;

        let buttonClassName = "cell_button"

        switch (status) {
            case CellStatus.Flagged:
                icon = <BsFlagFill className="cell_icon" size={iconSize} color='red'/>

                break;
            case CellStatus.Opened:
                if (isMine)
                    icon = <FaBomb className="cell_icon" size={iconSize} />
                
                buttonClassName += " open_cell_button"

                break;
            case CellStatus.Closed:
                break;
        }

        return <button className={buttonClassName}>{icon}</button>
    }
}
