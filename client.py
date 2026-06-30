import requests

_BASEURL = "http://ws.audioscrobbler.com/2.0/"


class UserInfo:
    def __init__(self, data):
        user = data["user"]
        self.name = user["name"]
        self.age = int(user["age"])
        self.realname = user["realname"]

        self.play_count = int(user["playcount"])
        self.artist_count = int(user["artist_count"])
        self.track_count = int(user["track_count"])
        self.album_count = int(user["album_count"])


class LastFMClient:
    def __init__(self, username, apikey):
        self.username = username
        self.apikey = apikey

    def _make_request(self, method):
        r = requests.get(
            _BASEURL,
            params={
                "method": method,
                "user": self.username,
                "api_key": self.apikey,
                "format": "json"
            },
        )
        r.raise_for_status()

        return r

    def getInfos(self):
        r = self._make_request("user.getinfo")
        data = r.json()

        return UserInfo(data)


if __name__ == "__main__":
    from dotenv import load_dotenv
    from os import getenv
    
    load_dotenv()

    client = LastFMClient(getenv("LASTFM_USERNAME"), getenv("LASTFM_APIKEY"))
    info = client.getInfos()
    
    print(f"{info.name} has {info.play_count} scrobbles")