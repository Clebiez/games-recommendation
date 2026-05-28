# Games Recommendation

Content-based game recommendation engine using TF-IDF and cosine similarity on genres, keywords, and summaries from IGDB data.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
uv sync
```

## Usage

### Get recommendations

Edit `gameIds` in `main.py` with IGDB game IDs, then:

```bash
uv run main.py
```

Outputs the top 10 most similar games based on a weighted score (keywords 30%, summaries 20%, rating 30%, genres 10%).

### Refresh game data from IGDB

Requires a [Twitch/IGDB API](https://api-docs.igdb.com/#getting-started) app:

```bash
cp .env.example .env
# Fill in SECRET_KEY and APP_CLIENT
uv run scripts/scrapper.py
```

This fetches all games and genres and writes `games.csv` / `genres.csv`.

## Project structure

```
main.py                              # Entry point, runs recommendations
domain/
  RecommendationFinder.py            # Recommendation engine (TF-IDF + cosine similarity)
infrastructure/
  CSVAdapter.py                      # Read/write CSV files
  GameAPIAdapter.py                  # IGDB API client
scripts/
  scrapper.py                        # Fetches data from IGDB API
data/
  games.csv                          # Game dataset
  genres.csv                         # Genre mapping
```

## How it works

1. Builds TF-IDF matrices for genres, keywords, and summaries
2. Computes cosine similarity between all games and the input games (N×k matrix, not N×N)
3. Averages similarity scores across input games
4. Combines scores with a weighted formula and returns top N
