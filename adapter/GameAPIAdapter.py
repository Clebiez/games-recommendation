from requests import post

BASE_API = "https://api.igdb.com/v4"
LIMIT = 100

GAMES_FIELD = "fields name, summary, total_rating, total_rating_count, first_release_date, game_type, game_status, genres, platforms; where game_type = 0 & total_rating_count > 5;"


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

    def queryGameStatuses(self):
        return self.post(f"{BASE_API}/game_statuses", "fields *; limit 100;")

    def queryGameGenres(self):
        return self.post(f"{BASE_API}/genres", "fields *; limit 100;")

    def countGames(self):
        return self.post(
            f"{BASE_API}/games/count",
            "fields *; where game_type = 0 & total_rating_count > 5;",
        )

    def queryGame(self, page: int):
        return self.post(
            f"{BASE_API}/games",
            f"{GAMES_FIELD} limit {LIMIT}; offset {page * LIMIT};",
        )
