import requests_oauthlib

from spt_webui_backend import schemas


def get_me(
        session: requests_oauthlib.OAuth2Session,
) -> schemas.SpotifyUser:
    return schemas.SpotifyUser.model_validate(session.get("https://api.spotify.com/v1/me").json())