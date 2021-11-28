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
            status: props.cell.status,
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

    render() {
        let { isMine } = this.props.cell;
        let { status } = this.state;

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

        console.log(`=== 000 (${this.props.cell.row}, ${this.props.cell.col}) ${this.state.status} ===`)

        // return <button className={buttonClassName}>{icon}</button>
        return <button onClick={this.handleOnClick} onContextMenu={this.handleOnContextmenu} className={buttonClassName}>{icon}</button>
    }
}
