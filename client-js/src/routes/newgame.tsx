import { useEffect, useState, MouseEvent, Suspense } from 'react';
import { Navigate, useNavigate, useParams } from 'react-router-dom';
import { getGameEndpoint, MinesweeperService } from '../api/api';
import { GameData } from '../api/types';
import { GameComponent } from '../components/game';
import { Link } from 'react-router-dom';
import { servicesVersion } from 'typescript';

interface NewgameRouteProps {
    service: MinesweeperService,
}

export function NewgameRoute(props: NewgameRouteProps): JSX.Element {

    let [error, setError] = useState<string | undefined>(undefined);
    let [gameCreating, setGameCreated] = useState<boolean>(false)
    let [gameId, setGameId] = useState<string | undefined>(undefined);

    const btnCreateGameHandler = (e:MouseEvent): void => {
      e.preventDefault();

      setGameCreated(true);

      let height = parseInt((document.getElementById("inputHeight") as HTMLInputElement).value);
      let width = parseInt((document.getElementById("inputWidth") as HTMLInputElement).value);
      let bombs = parseInt((document.getElementById("inputNumBombs") as HTMLInputElement).value);

      props.service.createGame(height,width,bombs)
        .then(
            id => setGameId(id),
            error => setError(error.message));
    };
    
    if (error !== undefined) {
        return (
            <div className="menu">
                <p>An error occured: error</p>
            </div>
        );
    } else if (gameId !== undefined) {
        return (
            <Navigate to={`/game/${gameId}`} replace={false}/>
        );
    } else if (gameCreating) {
        return (
            <div className="menu">
                <p>sit back and relax, your game is being generated</p>
            </div>
        );
    } else {
        return (
            <div className="menu">
            <Link className="menu-header" to="/">MultiMine</Link>
            <p>New Game Server</p>
            <br/>
            <label>Width</label>
            <input className="form-control" type="number" id="inputWidth"/>
      
            <br/>
            <label>Height</label>
            <input className="form-control" type="number" id="inputHeight"/>
      
            <br/>
            <label>Number of Bombs</label>
            <input className="form-control" type="number" id="inputNumBombs"/>
      
            <br/>
            <button className="btn btn-primary" onClick={btnCreateGameHandler}>Create Game</button>
            </div>
          );
    }
}
