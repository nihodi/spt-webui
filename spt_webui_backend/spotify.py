from requests_oauthlib import OAuth2Session

from spt_webui_backend import schemas


def get_me(
        session: OAuth2Session,
) -> schemas.SpotifyUser:
    return schemas.SpotifyUser.model_validate(session.get("https://api.spotify.com/v1/me").json())


def get_playback_state(
        session: OAuth2Session,
):
    resp = session.get("https://api.spotify.com/v1/me/player")
    if resp.status_code == 204:
        return None

    return resp.json()
