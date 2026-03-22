import pandas as pd



class RecommendationGetter:
    def __init__(self, gamesDF: pd.DataFrame, gameIds: list[int], cosin_genres, cosin_summaries):
        gamesDF = gamesDF.drop_duplicates(subset='id').reset_index(drop=True)
        self.gamesDF = gamesDF
        indices = pd.Series(gamesDF.index, index=gamesDF['id'])

        self.cosin_genres = cosin_genres
        self.cosin_summaries = cosin_summaries

        self.selectedGames = indices.reindex(gameIds)

        # Detect if some game ids are unknown (we don't have all games in the original DataFrame)
        missingIds = self.selectedGames[self.selectedGames.isna()].index.tolist()
        if missingIds:
            raise ValueError(f"Unknown game IDs: {missingIds}")


    def getByGenres(self):
        similarityScores = pd.DataFrame(self.cosin_genres[self.selectedGames].mean(axis=0), columns=["score_genres"])
        return self.filterInputGames(similarityScores, "score_genres")
    
    def getBySummary(self):
        computed = self.cosin_summaries[self.selectedGames]
        similarityScores = pd.DataFrame(computed.mean(axis=0), columns=["score_summaries"])
        return self.filterInputGames(similarityScores, "score_summaries")
    
    def filterInputGames(self, similarityScores: pd.DataFrame, key: str):
        # Remove the input games from the recommendations, then keep the best matches.
        gameIndices = similarityScores.drop(index=self.selectedGames).index
        recommendations = self.gamesDF.iloc[gameIndices].copy()
        recommendations[key] = similarityScores.loc[gameIndices, key].values
        return recommendations

    def getRecommendations(self, topN: int = 10):
        byGenres = self.getByGenres()
        bySummary = self.getBySummary()

        recommendations = byGenres.merge(
            bySummary[["id", "score_summaries"]],
            on="id",
            how="inner",
        )
        recommendations["score"] = recommendations["score_summaries"] * 0.7 + recommendations["score_genres"] * 0.2 + (recommendations["total_rating"] / 100) * 0.1

        return recommendations.sort_values('score', ascending=False).head(topN)

        
