import ast
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class RecommendationTrainer:
    def __init__(self, gamesDF):
        gamesDF = gamesDF.drop_duplicates(subset="id").reset_index(drop=True)
        self.gamesDF = gamesDF

    def getCosinSimilarityForGenres(self):
        # Parse "genres" : "[15, 16, 33]" -> [15, 16, 33]
        def parse_genres(x):
            if pd.isna(x) or str(x).strip() == "":
                return []
            return ast.literal_eval(str(x))

        self.gamesDF["genres_parsed"] = self.gamesDF["genres_normalized"].apply(
            parse_genres
        )

        # Binary matrice game x genre
        mlb = MultiLabelBinarizer()
        XBin = mlb.fit_transform(self.gamesDF["genres_parsed"])

        tfidf = TfidfTransformer()
        tfidf_matrix = tfidf.fit_transform(XBin)
        cosine_sim = cosine_similarity(tfidf_matrix)
        return pd.DataFrame(cosine_sim)

    def getCosinSimilarityForKeywords(self):
        # Parse "genres" : "[15, 16, 33]" -> [15, 16, 33]
        def parse_genres(x):
            if pd.isna(x) or str(x).strip() == "":
                return []
            return ast.literal_eval(str(x))

        self.gamesDF["keywords_parsed"] = self.gamesDF["keywords"].apply(parse_genres)

        # Binary matrice game x genre
        mlb = MultiLabelBinarizer()
        XBin = mlb.fit_transform(self.gamesDF["keywords_parsed"])

        tfidf = TfidfTransformer()
        tfidf_matrix = tfidf.fit_transform(XBin)
        cosine_sim = cosine_similarity(tfidf_matrix)
        return pd.DataFrame(cosine_sim)

    def getCosinSimilarityForSummary(self):
        tfidf = TfidfVectorizer(stop_words="english")

        tfidf_matrix = tfidf.fit_transform(
            self.gamesDF["summary"].fillna("").values.astype("U")
        )
        cosine_sim = cosine_similarity(tfidf_matrix)
        return pd.DataFrame(cosine_sim)
