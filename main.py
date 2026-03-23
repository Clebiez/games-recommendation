from adapter.CSVAdapter import CSVAdapter
from adapter.NumpyBinaryAdapter import NumpyBinaryAdapter
from time import perf_counter

from models.RecommendationGetter import RecommendationGetter
import pandas as pd


def print_section(title: str):
    line = "=" * 72
    print(f"\n{line}\n{title}\n{line}")


def format_for_console(
    df: pd.DataFrame, columns: list[str], rename_map: dict[str, str] | None = None
):
    formatted = df[columns].copy()

    for col in ["total_rating", "score", "score_genres", "score_summaries"]:
        if col in formatted.columns:
            formatted[col] = pd.to_numeric(formatted[col], errors="coerce").round(3)

    if rename_map:
        formatted = formatted.rename(columns=rename_map)

    return formatted.to_string(index=False, line_width=220)


def main():
    start_time = perf_counter()
    csvAdapter = CSVAdapter()
    numpyAdapter = NumpyBinaryAdapter()

    cosinGenres = numpyAdapter.read("cosin_genres")
    cosinSummaries = numpyAdapter.read("cosin_summary")
    cosinKeywords = numpyAdapter.read("cosin_keywords")

    gamesDF = csvAdapter.read("games")
    gameIds = [7046, 90558, 152127]
    getter = RecommendationGetter(
        gamesDF,
        gameIds,
        cosin_genres=cosinGenres,
        cosin_summaries=cosinSummaries,
        cosin_keywords=cosinKeywords,
    )

    print_section("INPUT GAMES")
    input_games = gamesDF[gamesDF["id"].isin(gameIds)]
    print(
        format_for_console(
            input_games,
            ["name", "genres_normalized", "total_rating"],
            {
                "name": "Game",
                "genres_normalized": "Genres",
                "total_rating": "Rating",
            },
        )
    )

    recommendations = getter.getRecommendations()
    elapsed_seconds = perf_counter() - start_time

    print_section("RECOMMENDED GAMES")
    print(
        format_for_console(
            recommendations,
            ["name", "genres_normalized", "total_rating", "score"],
            {
                "name": "Game",
                "genres_normalized": "Genres",
                "total_rating": "Rating",
                "score": "MatchScore",
            },
        )
    )
    print(f"Generation time: {elapsed_seconds:.4f} s")


if __name__ == "__main__":
    main()
