import json
import os
from datetime import datetime, timedelta
from typing import Optional

import pydantic
import requests
import requests_oauthlib

from spt_webui_backend import schemas
from spt_webui_backend.environment import ENVIRONMENT

current_token: Optional[schemas.AccessToken] = None

if os.path.isfile(ENVIRONMENT.token_save_location):
    with open(ENVIRONMENT.token_save_location, "r") as file:
        try:
            current_token = schemas.AccessToken.model_validate(json.load(file))
        except (pydantic.ValidationError, json.JSONDecodeError):
            print("failed to load token from file.")


def set_current_token(token: schemas.AccessToken) -> None:
    global current_token

    current_token = token
    # save to some file or something ig

    with open(ENVIRONMENT.token_save_location, "w") as file:
        file.write(str(token.model_dump_json()))
        print("saved token to file.")


def get_oauth_session(token: Optional[schemas.AccessToken] = None, force_refresh: bool = False) -> requests_oauthlib.OAuth2Session:
    if token is None:
        if not current_token:
            raise RuntimeError('No current token')
        token = current_token

    client = requests_oauthlib.OAuth2Session(
        ENVIRONMENT.spotify_client_id,
        redirect_uri=ENVIRONMENT.spotify_redirect_uri,
        token={
            "access_token": token.access_token,
            "token_type": "Bearer",
            "refresh_token": token.refresh_token,
        }
    )
    # if token is about to expire, request a new one
    if (token.expires_at - datetime.now()).total_seconds() < 300 or force_refresh:
        print("refreshing token")
        resp = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": token.refresh_token,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            auth=(ENVIRONMENT.spotify_client_id, ENVIRONMENT.spotify_client_secret)
        )
        resp.raise_for_status()

        access_token = resp.json()
        expires = datetime.now() + timedelta(seconds=access_token["expires_in"])

        token = schemas.AccessToken(
            access_token=access_token["access_token"],
            refresh_token=token.refresh_token,
            expires_at=expires)

        set_current_token(token)

        return get_oauth_session()

    return client


SPOTIFY_SCOPES = " ".join(["user-read-currently-playing", "user-modify-playback-state", "user-read-playback-state", "playlist-modify-public", "playlist-modify-private"])
