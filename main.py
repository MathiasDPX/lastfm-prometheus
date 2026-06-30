from prometheus_client import start_http_server, Gauge
from dotenv import load_dotenv
from time import sleep
from os import getenv
from client import *

load_dotenv()

LASTFM_USERNAME = getenv("LASTFM_USERNAME")
LASTFM_APIKEY = getenv("LASTFM_APIKEY")
SAMPLE_RATE = int(getenv("SAMPLE_RATE", 60))
HTTP_ADDR = getenv("HTTP_ADDR", "0.0.0.0")
HTTP_PORT = int(getenv("HTTP_PORT", 8000))

if LASTFM_USERNAME is None:
    print("Missing LASTFM_USERNAME environment variable")
    
if LASTFM_APIKEY is None:
    print("Missing LASTFM_APIKEY environment variable")


client = LastFMClient(LASTFM_USERNAME, LASTFM_APIKEY)

playCountGauge = Gauge("play_count", "Number of scrobbles")
artistCountGauge = Gauge("artist_count", "Number of unique artists scrobbled")
trackCountGauge = Gauge("track_count", "Number of unique tracks scrobbled")
albumCountGauge = Gauge("album_count", "Number of unique albums scrobbled")
trackGauge = Gauge("tracks", "Tracks", ["artist", "name"])
isPlayingGauge = Gauge("isplaying", "Is Playing")

if __name__ == "__main__":
    
    start_http_server(addr=HTTP_ADDR, port=HTTP_PORT)
    print(f"Running Prometheus exporter on {HTTP_ADDR}:{HTTP_PORT}")
    print(f"exporting {LASTFM_USERNAME}'s metrics")
    
    while True:
        info = client.getInfos()
        isPlaying = client.isPlaying()
        
        playCountGauge.set(info.play_count)
        artistCountGauge.set(info.artist_count)
        trackCountGauge.set(info.track_count)
        albumCountGauge.set(info.album_count)
        isPlayingGauge.set(int(isPlaying))
        
        # 1 <= limit <= 1000
        toptracks = client.getTopTracks(limit=1000)
        
        for track in toptracks:
            trackGauge.labels(
                artist=track.artist,
                name=track.name
            ).set(track.playcount)
        
        sleep(SAMPLE_RATE)