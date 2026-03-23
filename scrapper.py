from dotenv import load_dotenv
import os
from adapter.GameAPIAdapter import GameApiAdapter
from adapter.CSVAdapter import CSVAdapter
import pandas as pd

load_dotenv()  # reads variables from the .env file
secret_key = os.getenv("SECRET_KEY")
app_client = os.getenv("APP_CLIENT")


def main():
    gameAPI = GameApiAdapter(client_id=app_client, secret_key=secret_key)
    csvAdapter = CSVAdapter()

    genres = gameAPI.queryGameGenres()
    csvAdapter.write(data=genres, fileName="genres")
    gameStatuses = gameAPI.queryGameStatuses()
    csvAdapter.write(data=gameStatuses, fileName="status")

    games = gameAPI.queryAllGames()
    print(f"{len(games)} games loaded.")

    df_games = pd.DataFrame(games)
    df_genres = pd.DataFrame(genres).rename(
        columns={"id": "genre_id", "name": "genre_name"}
    )
    genre_map = df_genres.set_index("genre_id")["genre_name"]
    df_games["genres_normalized"] = df_games["genres"].apply(
        lambda ids: [
            genre_map[id]
            for id in (ids if isinstance(ids, list) else [])
            if id in genre_map
        ]
    )

    csvAdapter.write(data=df_games.to_dict(orient="records"), fileName="games")


if __name__ == "__main__":
    main()
