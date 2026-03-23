from dotenv import load_dotenv
import pandas as pd
from models.RecommendationTrainer import RecommendationTrainer
from adapter.NumpyBinaryAdapter import NumpyBinaryAdapter
from adapter.CSVAdapter import CSVAdapter


def main():
    csvAdapter = CSVAdapter()
    binaryAdapter = NumpyBinaryAdapter()

    gamesDF = csvAdapter.read("games")

    trainer = RecommendationTrainer(gamesDF)
    cosinSimGenres = trainer.getCosinSimilarityForGenres()
    binaryAdapter.write(cosinSimGenres, "cosin_genres")
    cosinSimKeywords = trainer.getCosinSimilarityForKeywords()
    binaryAdapter.write(cosinSimKeywords, "cosin_keywords")
    cosinSimSummary = trainer.getCosinSimilarityForSummary()
    binaryAdapter.write(cosinSimSummary, "cosin_summary")


if __name__ == "__main__":
    main()
