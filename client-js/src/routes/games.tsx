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

    // We only want this to run once so we don't watch any dependency values for updates
    useEffect(() => {
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    if (error !== undefined) {
        return <p>ERROR: {error}</p>
    } else if (! isLoaded) {
        return <p>loading...</p>
    } else if (games.length === 0) {
        return (
          <div className="menu">
            <Link className="menu-header" to="/">MultiMine</Link>

            <p>no games were found mathing the given criteria</p>
          </div>
      )
    } else {
        return (
          <div className="menu">
          <Link className="menu-header" to="/">MultiMine</Link><br/><br/>
            {
                games.map((game: GameData, i:number) => (
                        <p key={i}>
                            <Link className="menu-item" to={`/game/${game.id}`}>Minesweeper Game {i + 1}: {game.height} X {game.width} ({game.mineCount} mines) - Started at: {new Date(game.createdAt as any * 1000).toString()}</Link>
                            </p>
                    )
                )
            }
        </div>
      )
    }
}
