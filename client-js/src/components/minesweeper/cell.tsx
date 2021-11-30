import React from 'react';
import { BsFlagFill, BsSquare } from 'react-icons/bs';
import { FaBomb } from 'react-icons/fa';
import { Cell, CellStatus } from './types';

interface CellProps {
    cell: Cell,

    isFlagMode: boolean,

    cellUpdater: (rol: number, col: number, status: CellStatus) => void
}

interface CellState { }

// todo: could be a funcitonal compoennt
export class CellCommponent extends React.Component<CellProps, CellState> {
    constructor(props: CellProps) {
        super(props);

        this.state = { }
    }

    /**
     * Callback for when the user attempts to flag a cell.
     */
    flagCell = () => {
        switch (this.props.cell.status) {
            case CellStatus.Flagged:
                this.props.cellUpdater(this.props.cell.row, this.props.cell.col, CellStatus.Closed);
                break;
            case CellStatus.Opened:
                // do nothing...
                break;
            case CellStatus.Closed:
                this.props.cellUpdater(this.props.cell.row, this.props.cell.col, CellStatus.Flagged);
                break;
        }
    }

    /**
     * Callback for when a user attempts to open a cell.
     */
    openCell = () => {
        switch (this.props.cell.status) {
            case CellStatus.Flagged:
            case CellStatus.Opened:
                // do nothing...
                break;
            case CellStatus.Closed:
                this.props.cellUpdater(this.props.cell.row, this.props.cell.col, CellStatus.Opened);
                break;
        }
    }

    handleOnClick = () => {
        this.props.isFlagMode ? this.flagCell() : this.openCell();
    }

    handleOnContextmenu = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();

        this.props.isFlagMode ? this.openCell() : this.flagCell();

        return false
    }

    shouldComponentUpdate(nextProps: CellProps) {
        return nextProps.cell.status !== this.props.cell.status
    }

    /**
     * Get the JSX element body for an opened cell with at least 1 adjacent mine.
     * 
     * @returns a JSX element representing the amount of mines next to a cell.
     */
    private _getNumberElement(): JSX.Element {
        let className = `cell_mine_count open${this.props.cell.adjacentMines}`

        return <p className={className}>{this.props.cell.adjacentMines}</p>
    }

    render() {
        let { status, isMine, adjacentMines } = this.props.cell;

        let iconSize='20px'

        let icon = <BsSquare className="cell_icon" size={iconSize} />;

        let buttonClassName = "cell_button"

        switch (status) {
            case CellStatus.Flagged:
                icon = <BsFlagFill className="cell_icon" size={iconSize} color='red'/>

                break;
            case CellStatus.Opened:
                if (isMine) {
                    icon = <FaBomb className="cell_icon" size={iconSize} />
                } else if (adjacentMines > 0) {
                    icon = this._getNumberElement();
                } else {
                    icon = <p style={{visibility: 'hidden'}}>0</p>
                }
                
                buttonClassName += " open_cell_button"

                break;
            case CellStatus.Closed:
                break;
        }

        return <button onClick={this.handleOnClick} onContextMenu={this.handleOnContextmenu} className={buttonClassName}>{icon}</button>
    }
}
