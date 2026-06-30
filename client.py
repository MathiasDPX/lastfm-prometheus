import requests

_BASEURL = "http://ws.audioscrobbler.com/2.0/"


class Period:
    overall = "overall"

    def months(x: int):
        return f"{x}month"

    def days(x: int):
        return f"{x}day"


class UserInfo:
    def __init__(self, data):
        user = data["user"]
        self.name = user["name"]
        self.age = int(user["age"])
        self.realname = user["realname"]

        self.play_count = int(user.get("playcount", "0"))
        self.artist_count = int(user.get("artist_count", "0"))
        self.track_count = int(user.get("track_count", "0"))
        self.album_count = int(user.get("album_count", "0"))


class TopTrack:
    def __init__(self, data):
        self.name = data["name"]
        self.artist = data["artist"]["name"]
        self.rank = int(data["@attr"]["rank"])
        self.playcount = int(data.get("playcount", "0"))


class LastFMClient:
    def __init__(self, username, apikey):
        self.username = username
        self.apikey = apikey

    def _make_request(self, method, extraparams={}):
        params = {
            "method": method,
            "user": self.username,
            "api_key": self.apikey,
            "format": "json",
        }
        params.update(extraparams)
        r = requests.get(_BASEURL, params=params)

        r.raise_for_status()

        return r

    def getInfos(self):
        r = self._make_request("user.getinfo")
        data = r.json()

        return UserInfo(data)

    def getTopTracks(self, limit=50, page=1, period=Period.overall):
        params = {"limit": limit, "page": page, "period": period}
        r = self._make_request("user.gettoptracks", extraparams=params)
        data = r.json()

        return [TopTrack(trackdata) for trackdata in data["toptracks"]["track"]]


if __name__ == "__main__":
    from dotenv import load_dotenv
    from os import getenv

    load_dotenv()

    client = LastFMClient(getenv("LASTFM_USERNAME"), getenv("LASTFM_APIKEY"))
    info = client.getInfos()
    toptrack = client.getTopTracks(limit=1)[0]

    print(f"{info.name} has {info.play_count} scrobbles")
    print(
        f"Their most played track is {toptrack.name} by {toptrack.artist} with {toptrack.playcount} scrobbles"
    )
