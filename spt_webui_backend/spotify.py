import datetime
import urllib.parse
from typing import Dict, Tuple, Optional, Literal, List

import fastapi
import requests
from requests_oauthlib import OAuth2Session
from starlette import status

from spt_webui_backend import schemas, oauth2
from spt_webui_backend.schemas import SpotifyTrackObject


def get_track_id_from_shared_url(
        url: str
):
    # should look like this
    # https://open.spotify.com/track/398dL22bDbKbAmiOnPaq7o?si=ff5f409fcf8744b1
    url = urllib.parse.urlparse(url)

    return url.path[7:]


class Spotify:
    def __init__(self, session: Optional[OAuth2Session] = None):
        self._recently_requested_songs: List[Tuple[schemas.SpotifyTrackObject, datetime.datetime]] = []
        self._cache: Dict[str, Tuple[requests.Response, datetime.datetime]] = {}

        if not session:
            self.session = oauth2.get_oauth_session()
        else:
            self.session = session

    def get_playback_state(self) -> Optional[schemas.SpotifyPlaybackState]:
        resp = self._do_request("GET", "https://api.spotify.com/v1/me/player")
        if resp.status_code == 204:
            return None

        state = schemas.SpotifyPlaybackState.model_validate(resp.json())

        # if there is less than 15 seconds remaining of the song, set the cache expiration time to the remaining time
        if state.item.duration_ms - state.progress_ms < 15_000:
            try:
                resp, time = self._cache["GET https://api.spotify.com/v1/me/player"]
                time = datetime.datetime.now() + datetime.timedelta(seconds=(state.item.duration_ms - state.progress_ms) / 1000)
                print(f"less than 15 seconds remaining. settings cache time to {time}")
                self._cache["GET https://api.spotify.com/v1/me/player"] = (resp, time)

            except KeyError:
                pass

        return state

    def get_me(self) -> schemas.SpotifyUser:
        return schemas.SpotifyUser.model_validate(self._do_request("GET", "https://api.spotify.com/v1/me").json())

    def get_track_info(self, track_id: str) -> Optional[SpotifyTrackObject]:
        resp = self._do_request("GET", f"https://api.spotify.com/v1/tracks/{track_id}")
        resp.raise_for_status()

        return schemas.SpotifyTrackObject.model_validate(resp.json())

    def track_is_in_queue(self, uri: str) -> bool:
        for track, _ in self._recently_requested_songs:
            if track.uri == uri:
                return True

        return False

    def get_playback_queue(self) -> schemas.SpotifyQueue:
        resp = schemas.SpotifyQueue.model_validate(
            self._do_request("GET", "https://api.spotify.com/v1/me/player/queue").json())

        found_index = 0
        new_queue = []
        for track, time in self._recently_requested_songs:
            if resp.queue[found_index].uri == track["uri"]:
                new_queue.append((track, time))
                found_index += 1
            else:
                continue

        # remove songs no longer in the queue
        self._recently_requested_songs = new_queue

        return resp

    def add_track_to_queue(self, uri: str) -> schemas.SpotifyTrackObject:
        resp = self._do_request(
            "POST",
            "https://api.spotify.com/v1/me/player/queue?" + urllib.parse.urlencode({"uri": uri}),
            False
        )
        resp.raise_for_status()

        track_data = self.get_track_info(uri[14:])
        self._recently_requested_songs.append((track_data, datetime.datetime.now()))

        # try to remove queue cache because it just changed
        try:
            self._cache.pop("GET https://api.spotify.com/v1/me/player/queue")
        except KeyError:
            pass

        return track_data

    def _do_request(
            self,
            method: Literal["GET", "POST"],
            url: str,
            can_cache: bool = True,
            **kwargs
    ) -> requests.Response:
        if can_cache:
            cache = self._cache.get(f"{method} {url}")

            if cache is not None:
                (resp, timestamp) = cache
                # if less than 15 seconds have passed, return cache
                print(f"returned cached response for url: {method} {url}")
                if (datetime.datetime.now() - timestamp).total_seconds() <= 0:
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
            self._cache[f"{method} {url}"] = (resp, datetime.datetime.now() + datetime.timedelta(seconds=15))

        return resp

    def _refresh_token(self):
        self.session = oauth2.get_oauth_session(force_refresh=True)


spotify_instance: Optional[Spotify] = None


def get_spotify_instance() -> Spotify:
    global spotify_instance

    if spotify_instance is not None:
        return spotify_instance

    try:
        session = oauth2.get_oauth_session()
    except RuntimeError:
        raise fastapi.HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail="Could not get a Spotify instance")

    spotify_instance = Spotify(session)
    return spotify_instance
