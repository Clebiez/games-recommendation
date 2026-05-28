import pandas as pd
from thefuzz import fuzz


class GameRepository:
    def __init__(self, gamesDF: pd.DataFrame):
        self.gamesDF = gamesDF

    def search(self, query: str, limit: int = 10, threshold: int = 80) -> pd.DataFrame:
        """Fuzzy search on game names. Returns top matches above the score threshold."""
        scores = self.gamesDF["name"].apply(
            lambda name: fuzz.WRatio(query.lower(), str(name).lower())
        )
        results = self.gamesDF.copy()
        results["match_score"] = scores
        return (
            results[results["match_score"] >= threshold]
            .sort_values("match_score", ascending=False)
            .head(limit)
            .drop(columns=["match_score"])
        )
