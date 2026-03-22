from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def getGamesRecommendation(gamesDF, gameIds: list[int], top_n: int = 10):
    gamesDF = gamesDF.drop_duplicates(subset='id').reset_index(drop=True)
    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(gamesDF['summary'].fillna('').values.astype('U'))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    if isinstance(gameIds, int):
        gameIds = [gameIds]

    # Find Game Index by ID
    indices = pd.Series(gamesDF.index, index=gamesDF['id'])
    selectedGames = indices.reindex(gameIds)

    missingIds = selectedGames[selectedGames.isna()].index.tolist()
    if missingIds:
        raise ValueError(f"Unknown game IDs: {missingIds}")
    # Average similarity scores across all input games to build a combined profile.
    # Also ponderate based on multiple similarities
    similarityScores = pd.DataFrame(cosine_sim[selectedGames].mean(axis=0) * 0.8 + cosine_sim[selectedGames].sum(axis=0) * 0.2, columns=["score"])

    # Remove the input games from the recommendations, then keep the best matches.
    gameIndices = (
        similarityScores
        .drop(index=selectedGames)
        .sort_values("score", ascending=False)
        .head(top_n)
        .index
    )

    recommendations = gamesDF.iloc[gameIndices].copy()
    recommendations["score"] = similarityScores.loc[gameIndices, "score"].values
    return recommendations


def main():
    gamesDF = pd.read_csv('./games.csv')
    # gameIds = [1942, 9254, 152127, 36198, 109455]
    gameIds = [1942, 9254, 152127, 136625]
    print("Input games:")
    print(gamesDF[gamesDF['id'].isin(gameIds)][["id", "name", "summary", "total_rating"]])
    recommendations = getGamesRecommendation(gamesDF, gameIds)
    print("Output games:")
    print(recommendations[["id", "name", "summary", "total_rating", "score"]])


if __name__ == "__main__":
    main()
