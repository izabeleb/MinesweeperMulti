import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { MinesweeperService } from '../api/api';
import { GameData } from '../api/types';

interface GamesRouteProps {
    service: MinesweeperService,
}

export function GamesRoute(props: GamesRouteProps): JSX.Element {
    let [searchParams] = useSearchParams();
    let page = searchParams.get("page");
    let size = searchParams.get("size");

    let [error, setError] = useState<string | undefined>(undefined);
    let [games, setGames] = useState<GameData[]>([]);
    let [isLoaded, setIsLoaded] = useState<boolean>(false);

    useEffect(() => {
        console.log()
        props.service.getGames(
            page !== null ? parseInt(page) : undefined,
            size !== null ? parseInt(size) : undefined)
                .then(
                    page => {
                        setGames(page.data);
                        setIsLoaded(true);
                    },
                    error => {
                        setError(error.message);
                        setIsLoaded(true);
                    }
                )
    });

    if (error !== undefined) {
        return <p>ERROR: {error}</p>
    } else if (! isLoaded) {
        return <p>loading...</p>
    } else if (games.length === 0) {
        return <p>no games were found mathing the given criteria</p>
    } else {
        return <ul>
            {
                games.map((game: GameData, i:number) => <li key={i}><Link to={`/game/${game.id}`}>{game.id}</Link></li>)
            }
        </ul>
    }
}
