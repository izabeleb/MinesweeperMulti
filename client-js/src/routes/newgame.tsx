import { useEffect, useState, MouseEvent, Suspense } from 'react';
import { useParams } from 'react-router-dom';
import { MinesweeperService } from '../api/api';
import { GameData } from '../api/types';
import { GameComponent } from '../components/game';
import { Link } from 'react-router-dom';

interface NewgameRouteProps {
    service: MinesweeperService,
}

export function NewgameRoute(props: NewgameRouteProps): JSX.Element {

    let params = useParams();
    let shouldRedirect = true;
    let id = '';

    const btnCreateGameHandler = (e:MouseEvent): void => {
      e.preventDefault();

      let height = parseInt((document.getElementById("inputHeight") as HTMLInputElement).value);
      let width = parseInt((document.getElementById("inputWidth") as HTMLInputElement).value);
      let bombs = parseInt((document.getElementById("inputNumBombs") as HTMLInputElement).value);

      //let height = document.getElementById("inputHeight").value;
      //let numBombs = document.getElementById("inputNumBombs").value;
      //alert(width);



      let id = props.service.createGame(height,width,bombs);

    }

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
