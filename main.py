from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()
LASTFM_USERNAME = getenv('LASTFM_USERNAME')
LASTFM_APIKEY = getenv('6f54fff8d829774523703f22cbfd3f65')

def getInfos(username):
    r = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&user={username}&api_key={LASTFM_APIKEY}&format=json")
    r.raise_for_status()
    data = r.json()
    
    return data['user']

if __name__ == "__main__":
    print()