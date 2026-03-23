from requests import post
import time

BASE_API = "https://api.igdb.com/v4"
LIMIT = 100

GAMES_FIELD = "fields name, summary, total_rating, total_rating_count, keywords, game_type, game_status, genres, platforms; where game_type = (0, 4) & total_rating_count > 2;"


class GameApiAdapter:
    client_id: str
    secret_key: str
    access_token: str

    def __init__(self, client_id: str, secret_key: str):
        self.client_id = client_id
        self.secret_key = secret_key
        self.authenticate()

    def getHeaders(self):
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }

    def post(self, url, data: str):
        response = post(
            url,
            **{
                "headers": self.getHeaders(),
                "data": data,
            },
        )
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Error details: {response.text}")
        else:
            data = response.json()
            return data

    def authenticate(self):
        req = post(
            f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.secret_key}&grant_type=client_credentials"
        )
        self.access_token = req.json()["access_token"]

    def iterateOverPages(self, method):
        i = 0
        items = []

        while True:
            print(f"Page {i}: Number of items {len(items)}")
            lastAnswer = method(i)
            i += 1

            if len(lastAnswer) == 0:
                break
            else:
                items.extend(lastAnswer)
            time.sleep(0.25)

        return items

    def queryGameStatuses(self):
        return self.post(f"{BASE_API}/game_statuses", "fields *; limit 100;")

    def queryGameKeywords(self, page: int):
        return self.post(
            f"{BASE_API}/keywords", f"fields *; limit 100;; offset {page * LIMIT};"
        )

    def queryGameGenres(self):
        return self.post(f"{BASE_API}/genres", "fields *; limit 100;")

    def countGames(self):
        return self.post(f"{BASE_API}/games/count", GAMES_FIELD)

    def queryGame(self, page: int):
        return self.post(
            f"{BASE_API}/games",
            f"{GAMES_FIELD} limit {LIMIT}; offset {page * LIMIT};",
        )

    def queryAllGames(self):
        countGames = self.countGames()
        print(f"{countGames} to load:")
        games = self.iterateOverPages(self.queryGame)
        return games

    def queryAllKeywords(self):
        keywords = self.iterateOverPages(self.queryGameKeywords)
        return keywords
