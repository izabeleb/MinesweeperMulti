import React from 'react';
import { BsFlagFill, BsSquare } from 'react-icons/bs';
import { FaBomb } from 'react-icons/fa';
import { Cell, CellStatus } from './types';

interface CellProps {
    cell: Cell,
    is_flag_mode: boolean,
}

interface CellState {
    status: CellStatus,
}

export class CellCommponent extends React.Component<CellProps, CellState> {

    constructor(props: CellProps) {
        super(props)

        this.state = {
            // status: props.cell.status,
            status: CellStatus.Opened,
        }
    }

    /**
     * Callback for when the user attempts to flag a cell.
     */
    flagCell = () => {
        switch (this.state.status) {
            case CellStatus.Flagged:
                this.setState({status: CellStatus.Closed});
                break;
            case CellStatus.Opened:
                // do nothing...
                break;
            case CellStatus.Closed:
                this.setState({status: CellStatus.Flagged});
                break;
        }
    }

    /**
     * Callback for when a user attempts to open a cell.
     */
    openCell = () => {
        switch (this.state.status) {
            case CellStatus.Flagged:
            case CellStatus.Opened:
                // do nothing...
                break;
            case CellStatus.Closed:
                this.setState({status: CellStatus.Opened});
                break;
        }
    }

    handleOnClick = () => {
        this.props.is_flag_mode ? this.flagCell() : this.openCell();
    }

    handleOnContextmenu = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();

        this.props.is_flag_mode ? this.openCell() : this.flagCell();

        return false
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
        let { isMine, adjacentMines } = this.props.cell;
        let { status } = this.state;

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
