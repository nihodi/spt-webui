from typing import Optional
import datetime

import fastapi
import urllib.parse

import requests_oauthlib

from spt_webui_backend.environment import ENVIRONMENT
from spt_webui_backend import oauth2, spotify
from spt_webui_backend.schemas import AccessToken

app = fastapi.FastAPI()

# TODO: maybe refactor into a FastAPI dependency
try:
    Spotify = spotify.Spotify()
except Exception as e:
    pass


@app.get("/auth/callback")
def spotify_auth_callback(
        code: Optional[str] = None,
        error: Optional[str] = None,
):
    if code is None:
        raise fastapi.HTTPException(status_code=401, detail=error)

    session = requests_oauthlib.OAuth2Session(
        ENVIRONMENT.spotify_client_id,
        redirect_uri=ENVIRONMENT.spotify_redirect_uri,
    )

    token = session.fetch_token(
        "https://accounts.spotify.com/api/token",
        code,
        client_secret=ENVIRONMENT.spotify_client_secret,
    )

    expires = datetime.datetime.now() + datetime.timedelta(seconds=token["expires_in"])
    token = AccessToken(access_token=token["access_token"], refresh_token=token["refresh_token"], expires_at=expires)

    session = oauth2.get_oauth_session(token)
    tmp_spotify = spotify.Spotify(session)
    user = tmp_spotify.get_me()

    if user.id != ENVIRONMENT.spotify_allowed_account_id:
        raise fastapi.HTTPException(status_code=401, detail="You are not allowed here ;)")

    global Spotify
    oauth2.set_current_token(token)
    Spotify = spotify.Spotify()


@app.get("/auth/setup")
def spotify_auth_setup():
    return fastapi.responses.RedirectResponse("https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
        "client_id": ENVIRONMENT.spotify_client_id,
        "response_type": "code",
        "redirect_uri": ENVIRONMENT.spotify_redirect_uri,
        "scope": oauth2.SPOTIFY_SCOPES,
    }))


@app.get("/playback/state")
def get_spotify_playback_state():
    return Spotify.get_playback_state()


# TODO: VALIDATE URL!!
@app.post("/playback/queue")
def add_spotify_queue_item(
        url: str
):
    session = oauth2.get_oauth_session()
    track_id = spotify.get_track_id_from_shared_url(url)
    spotify.add_track_to_queue(session, f"spotify:track:{track_id}")


@app.get("/playback/queue")
def get_spotify_playback_queue():
    return Spotify.get_playback_queue()
