from prometheus_client import start_http_server, Gauge
from dotenv import load_dotenv
from time import sleep
from os import getenv
from client import *

load_dotenv()

LASTFM_USERNAME = getenv("LASTFM_USERNAME")
LASTFM_APIKEY = getenv("LASTFM_APIKEY")

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

if __name__ == "__main__":
    addr = "0.0.0.0"
    port = 8000
    
    start_http_server(addr=addr, port=port)
    print(f"Running Prometheus exporter on {addr}:{port}")
    print(f"exporting {LASTFM_USERNAME}'s metrics")
    
    while True:
        info = client.getInfos()
        
        playCountGauge.set(info.play_count)
        artistCountGauge.set(info.artist_count)
        trackCountGauge.set(info.track_count)
        albumCountGauge.set(info.album_count)
        
        # 1 <= limit <= 1000
        toptracks = client.getTopTracks(limit=1000)
        
        for track in toptracks:
            trackGauge.labels(
                artist=track.artist,
                name=track.name
            ).set(track.playcount)
        
        sleep(60)