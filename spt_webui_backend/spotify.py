import datetime
import urllib.parse
from typing import Dict, Tuple, Optional, Literal, List

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


class Spotify:
    def __init__(self, session: Optional[OAuth2Session] = None):
        self._recently_requested_songs: List[Tuple[str, datetime.datetime]] = []
        self._cache: Dict[str, Tuple[requests.Response, datetime.datetime]] = {}

        if not session:
            self.session = oauth2.get_oauth_session()
        else:
            self.session = session

    def get_playback_state(self):
        resp = self._do_request("GET", "https://api.spotify.com/v1/me/player")
        if resp.status_code == 204:
            return None

        return resp.json()

    def get_me(self) -> schemas.SpotifyUser:
        return schemas.SpotifyUser.model_validate(self._do_request("GET", "https://api.spotify.com/v1/me").json())

    def get_playback_queue(self):
        resp = self._do_request("GET", "https://api.spotify.com/v1/me/player/queue").json()

        for track in resp["queue"]:
            track["is_in_queue"] = False

        matching_index = 0
        print(self._recently_requested_songs)

        # FIXME: kinda does not work if the same song is in the queue multiple times i think
        for i, track in enumerate(resp["queue"]):
            matching_recent_songs = [tr for tr in self._recently_requested_songs if tr[0] == track["uri"]]
            if len(matching_recent_songs) > 0:
                track["is_in_queue"] = True
            else:
                break

            matching_index = i

        # remove songs no longer in the queue
        self._recently_requested_songs = self._recently_requested_songs[len(self._recently_requested_songs) - matching_index:]

        return resp

    def add_track_to_queue(self, uri: str):
        resp = self._do_request(
            "POST",
            "https://api.spotify.com/v1/me/player/queue?" + urllib.parse.urlencode({"uri": uri}),
            False
        )
        resp.raise_for_status()

        self._recently_requested_songs.append((uri, datetime.datetime.now()))

        # try to remove queue cache because it just changed
        try:
            self._cache.pop("GET https://api.spotify.com/v1/me/player/queue")
        except KeyError:
            pass

    def _do_request(self, method: Literal["GET", "POST"], url: str, can_cache: bool = True,
                    **kwargs) -> requests.Response:
        if can_cache:
            cache = self._cache.get(f"{method} {url}")

            if cache is not None:
                (resp, timestamp) = cache
                # if less than 15 seconds have passed, return cache
                print(f"returned cached response for url: {method} {url}")
                if (datetime.datetime.now() - timestamp).total_seconds() < 15:
                    return resp

                # remove from cache if more than 15 seconds have passed
                self._cache.pop(f"{method} {url}")

        match method:
            case "GET":
                fn = self.session.get
            case "POST":
                fn = self.session.post
            case _:
                raise ValueError("Unsupported method")

        resp = fn(url, **kwargs)

        # retry once if access token is invalid
        if resp.status_code == 401:
            self._refresh_token()
            resp = fn(url, **kwargs)

        resp.raise_for_status()

        if can_cache:
            self._cache[f"{method} {url}"] = (resp, datetime.datetime.now())

        return resp

    def _refresh_token(self):
        self.session = oauth2.get_oauth_session()
