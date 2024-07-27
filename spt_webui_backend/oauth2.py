import os
import json
from datetime import datetime
from typing import Optional

import pydantic
import requests_oauthlib

from spt_webui_backend import schemas
from spt_webui_backend.environment import ENVIRONMENT

current_token: Optional[schemas.AccessToken] = None

if os.path.isfile("saved_token"):
    with open("saved_token", "r") as file:
        try:
            current_token = schemas.AccessToken.model_validate(json.load(file))
        except (pydantic.ValidationError, json.JSONDecodeError):
            print("failed to load token from file.")


def set_current_token(token: schemas.AccessToken) -> None:
    global current_token

    current_token = token
    # save to some file or something ig

    with open("saved_token", "w") as file:
        file.write(str(token.model_dump_json()))
        print("saved token to file.")


def get_oauth_session(token: Optional[schemas.AccessToken] = None) -> requests_oauthlib.OAuth2Session:
    if token is None:
        if not current_token:
            raise Exception('No current token')
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
    if (token.expires_at - datetime.now()).total_seconds() < 180:
        print("refreshing access token")
        client.refresh_token("https://accounts.spotify.com/api/token")

    return client


SPOTIFY_SCOPES = " ".join(["user-read-currently-playing", "user-modify-playback-state", "user-read-playback-state"])