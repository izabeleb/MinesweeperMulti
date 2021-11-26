import React from 'react';
import { Cell, CellCommponent } from './cell';

interface MinefieldProps {
    cells: Cell[][]
}

interface MinefieldState { }

export class MinefieldCommponent extends React.Component<MinefieldProps, MinefieldState> {
    constructor(props: MinefieldProps) {
        super(props)

        this.state = { }
    }
    
    render() {
        let cells = this.props.cells;

        return <div className="window minefield">
            {
                cells.map(row => <tr>
                        {
                            row.map(cell => <td key={10}> <CellCommponent cell={cell} /> </td>)
                        }
                    </tr>
                )
            }
        </div>
    }
}