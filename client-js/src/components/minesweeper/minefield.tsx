import React from 'react';
import { CellCommponent } from './cell';
import { Cell } from './types';

interface MinefieldProps {
    cells: Cell[][],
    is_flag_mode: boolean,
}

interface MinefieldState { }

export class MinefieldCommponent extends React.Component<MinefieldProps, MinefieldState> {
    constructor(props: MinefieldProps) {
        super(props)

        this.state = { }
    }
    
    render() {
        let cells = this.props.cells;

        return <table className="window minefield">
            <tbody>
                {
                    cells.map((row: Cell[], i: number) =>
                        <tr key={i}>
                            {
                                row.map((cell: Cell, j: number) =>
                                    <td key={j}>
                                        <CellCommponent cell={cell} is_flag_mode={this.props.is_flag_mode} />
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