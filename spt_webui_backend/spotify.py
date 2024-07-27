import datetime
import urllib.parse
from typing import Dict, Tuple, Optional

import requests
from requests_oauthlib import OAuth2Session

from spt_webui_backend import schemas, oauth2


def get_track_id_from_shared_url(
        url: str
):
    # should look like this
    # https://open.spotify.com/track/398dL22bDbKbAmiOnPaq7o?si=ff5f409fcf8744b1
    url = urllib.parse.urlparse(url)

    return url.path[7:]


# TODO: refactor the rest of these functions into the class
def add_track_to_queue(
        session: OAuth2Session,
        uri: str
):
    resp = session.post("https://api.spotify.com/v1/me/player/queue?" + urllib.parse.urlencode({"uri": uri}))
    resp.raise_for_status()


class Spotify:
    _get_cache: Dict[str, Tuple[requests.Response, datetime.datetime]] = {}

    def __init__(self, session: Optional[OAuth2Session] = None):
        if not session:
            self.session = oauth2.get_oauth_session()
        else:
            self.session = session

    def get_playback_state(self):
        resp = self._do_get_request("https://api.spotify.com/v1/me/player")
        if resp.status_code == 204:
            return None

        return resp.json()

    def get_me(self) -> schemas.SpotifyUser:
        return schemas.SpotifyUser.model_validate(self._do_get_request("https://api.spotify.com/v1/me").json())

    def get_playback_queue(self):
        return self._do_get_request("https://api.spotify.com/v1/me/player/queue").json()

    def _do_get_request(self, url: str, can_cache: bool = True, **kwargs) -> requests.Response:
        if can_cache:
            cache = self._get_cache.get(url)

            if cache is not None:
                (resp, timestamp) = cache
                # if less than 15 seconds have passed, return cache
                print("returned cached response for url: " + url)
                if (datetime.datetime.now() - timestamp).total_seconds() < 15:
                    return resp

        resp = self.session.get(url, **kwargs)

        # retry once if access token is invalid
        if resp.status_code == 401:
            self._refresh_token()
            resp = self.session.get(url, **kwargs)

        resp.raise_for_status()

        if can_cache:
            self._get_cache[url] = (resp, datetime.datetime.now())

        return resp

    def _refresh_token(self):
        self.session = oauth2.get_oauth_session()
