import urllib.parse

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


def get_track_id_from_shared_url(
        url: str
):
    # should look like this
    # https://open.spotify.com/track/398dL22bDbKbAmiOnPaq7o?si=ff5f409fcf8744b1
    url = urllib.parse.urlparse(url)

    return url.path[7:]


def add_track_to_queue(
        session: OAuth2Session,
        uri: str
):
    resp = session.post("https://api.spotify.com/v1/me/player/queue?" + urllib.parse.urlencode({"uri": uri}))
    resp.raise_for_status()
