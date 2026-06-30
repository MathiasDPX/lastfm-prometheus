from dotenv import load_dotenv
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

if __name__ == "__main__":
    pass