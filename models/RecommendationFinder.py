from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import ast


class RecommendationFinder:
    def __init__(
        self,
        gamesDF: pd.DataFrame,
        gameIds: list[int],
    ):
        gamesDF = gamesDF.drop_duplicates(subset="id").reset_index(drop=True)
        self.gamesDF = gamesDF
        indices = pd.Series(gamesDF.index, index=gamesDF["id"])

        self.selectedGames = indices.reindex(gameIds)

        # Detect if some game ids are unknown (we don't have all games in the original DataFrame)
        missingIds = self.selectedGames[self.selectedGames.isna()].index.tolist()
        if missingIds:
            raise ValueError(f"Unknown game IDs: {missingIds}")

        self.selectedIndices = self.selectedGames.values

        self.tfidf_genres = self.__buildTfidfForArrays("genres")
        self.tfidf_keywords = self.__buildTfidfForArrays("keywords")
        self.tfidf_summaries = self.__buildTfidfForSummaries()

    # Parse "genres" : "[15, 16, 33]" -> [15, 16, 33]
    def __parse_array(self, x):
        if pd.isna(x) or str(x).strip() == "":
            return []
        return ast.literal_eval(str(x))

    def __buildTfidfForArrays(self, field: str):
        self.gamesDF[f"{field}_parsed"] = self.gamesDF[field].apply(self.__parse_array)

        mlb = MultiLabelBinarizer()
        XBin = mlb.fit_transform(self.gamesDF[f"{field}_parsed"])

        tfidf = TfidfTransformer()
        return tfidf.fit_transform(XBin)

    def __buildTfidfForSummaries(self):
        tfidf = TfidfVectorizer(stop_words="english")
        return tfidf.fit_transform(
            self.gamesDF["summary"].fillna("").values.astype("U")
        )

    def __getScores(self, tfidf_matrix, column_name: str):
        sim = cosine_similarity(tfidf_matrix, tfidf_matrix[self.selectedIndices])
        scores = sim.mean(axis=1)

        result = self.gamesDF.copy()
        result[column_name] = scores
        return result.drop(index=self.selectedIndices)

    def getRecommendations(self, topN: int = 10):
        byGenres = self.__getScores(self.tfidf_genres, "score_genres")
        byKeywords = self.__getScores(self.tfidf_keywords, "score_keywords")
        bySummary = self.__getScores(self.tfidf_summaries, "score_summaries")

        recommendations = byKeywords.merge(
            bySummary[["id", "score_summaries"]],
            on="id",
            how="inner",
        ).merge(byGenres[["id", "score_genres"]], on="id", how="inner")

        recommendations["score"] = (
            recommendations["score_summaries"] * 0.2
            + recommendations["score_genres"] * 0.1
            + recommendations["score_keywords"] * 0.3
            + (recommendations["total_rating"] / 100) * 0.3
        )

        return recommendations.sort_values("score", ascending=False).head(topN)
