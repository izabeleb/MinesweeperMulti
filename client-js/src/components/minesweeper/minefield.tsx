import React from 'react';
import { CellCommponent } from './cell';
import { Cell, CellStatus } from './types';

interface MinefieldProps {
    cells: Cell[][],

    isFlagMode: boolean,

    isActive: boolean,

    cellUpdater: (rol: number, col: number, status: CellStatus) => void
}

interface MinefieldState { }

export class MinefieldCommponent extends React.Component<MinefieldProps, MinefieldState> {
    constructor(props: MinefieldProps) {
        super(props)

        this.state = { }
    }
    
    render() {
        let { cells, isActive } = this.props;

        return <table className="window minefield">
            <tbody>
                {
                    cells.map((row: Cell[], i: number) =>
                        <tr key={i}>
                            {
                                row.map((cell: Cell, j: number) =>
                                    <td key={j}>
                                        <CellCommponent
                                            cellUpdater={this.props.cellUpdater}
                                            cell={cell}
                                            isFlagMode={this.props.isFlagMode}
                                            isActive={isActive} />
                                    </td>
                                )
                            }
                        </tr>
                    )
                }
            </tbody>
        </table>
    }
}