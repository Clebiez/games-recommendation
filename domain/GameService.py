import pandas as pd

from domain.RecommendationFinder import RecommendationFinder
from infrastructure.GameRepository import GameRepository


class GameService:
    def __init__(self, gamesDF: pd.DataFrame):
        self.gamesDF = gamesDF
        self.gameRepository = GameRepository(gamesDF)

    def search(self, query: str, limit: int = 10) -> list[dict]:
        results = self.gameRepository.search(query, limit=limit)
        return results[["id", "name", "genres", "summary", "total_rating", "cover_url", "slug"]].to_dict(
            orient="records"
        )

    def get_recommendations(self, game_ids: list[int]) -> list[dict]:
        finder = RecommendationFinder(self.gamesDF, game_ids)
        recommendations = finder.getRecommendations()
        return recommendations[
            ["id", "name", "genres", "summary", "total_rating", "score", "cover_url", "slug"]
        ].to_dict(orient="records")
