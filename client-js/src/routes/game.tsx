import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { MinesweeperService } from '../api/api';
import { GameData } from '../api/types';
import { GameComponent } from '../components/game';

interface GameRouteProps {
    service: MinesweeperService,
}

export function GameRoute(props: GameRouteProps): JSX.Element {
    let params = useParams();

    let [error, setError] = useState<string | undefined>(undefined);
    let [gameData, setGameData] = useState<GameData | undefined>(undefined);
    let [isLoaded, setIsLoaded] = useState<boolean>(false);

    // We only want this to run once so we don't watch any dependency values for updates
    useEffect(() => {
        props.service.getGame(params.id!)
            .then(
                gameData => {
                    setGameData(gameData);
                    setIsLoaded(true);
                },
                error => {
                    setError(error.message);
                    setIsLoaded(true);
                }
            )
    // eslint-disable-next-line react-hooks/exhaustive-deps
}, []);

    if (error !== undefined) {
        return <p>ERROR: {error} </p>
    } else if (! isLoaded) {
        return <p>loading...</p>
    } else if (gameData !== undefined) {
        return <GameComponent service={props.service} gameData={gameData} />
    } else {
        throw new Error("game should not be undefined");
    }
}