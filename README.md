# Last.fm Prometheus exporter

Prometheus exporter for [Last.fm](https://www.last.fm/)


## Installation

Create a `.env` file and populate it. You can get an api key [here](https://www.last.fm/api/account/create)

```toml
LASTFM_USERNAME=""
LASTFM_APIKEY=""
SAMPLE_RATE=60 # in seconds
```

`SAMPLE_RATE` is the interval in seconds between each pull from Last.fm API

Create a `docker-compose.yml` and run it

```yml
services:
  lastfm-prometheus:
    image: ghcr.io/mathiasdpx/lastfm-prometheus:latest
    container_name: lastfm-prometheus
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8000:8000"
```