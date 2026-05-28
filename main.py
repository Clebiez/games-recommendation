from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from infrastructure.CSVAdapter import CSVAdapter
from domain.GameService import GameService

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

csvAdapter = CSVAdapter()
gamesDF = csvAdapter.read("games")
gameService = GameService(gamesDF)


class RecommendationRequest(BaseModel):
    game_ids: list[int]


class GameResult(BaseModel):
    id: int
    name: str
    genres: str
    summary: str | None
    total_rating: float
    cover_url: str | None
    slug: str | None


class RecommendationResult(BaseModel):
    id: int
    name: str
    genres: str
    summary: str | None
    total_rating: float
    score: float
    cover_url: str | None
    slug: str | None


@app.get("/search", tags=["Search"])
def search(
    q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=50)
) -> list[GameResult]:
    return gameService.search(q, limit=limit)


@app.post("/get-recommendations", tags=["Recommendations"])
def get_recommendations(body: RecommendationRequest) -> list[RecommendationResult]:
    return gameService.get_recommendations(body.game_ids)


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")