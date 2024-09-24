import datetime
from typing import Literal, List, Optional, Tuple

from pydantic import BaseModel


class AccessToken(BaseModel):
    access_token: str
    refresh_token: str

    expires_at: datetime.datetime


class SpotifyUser(BaseModel):
    id: str


class User(BaseModel):
    id: int
    discord_user_id: int
    discord_display_name: str


class SpotifyExternalUrls(BaseModel):
    spotify: str


class SpotifySimplifiedArtistObject(BaseModel):
    href: str
    id: str
    uri: str

    name: str
    type: Literal["artist"]

    external_urls: SpotifyExternalUrls


class SpotifyImageObject(BaseModel):
    url: str
    width: int
    height: int


class SpotifyTrackObject(BaseModel):
    id: str

    duration_ms: int
    name: str
    popularity: int
    explicit: bool

    artists: List[SpotifySimplifiedArtistObject]

    external_urls: SpotifyExternalUrls
    href: str
    uri: str

    type: Literal["track"]

    is_local: bool

    class Album(BaseModel):
        id: str
        album_type: Literal["album", "single", "compilation"]
        total_tracks: int

        external_urls: SpotifyExternalUrls
        href: str
        uri: str

        images: List[SpotifyImageObject]

        name: str
        release_date: str
        type: Literal["album"]


    album: Album


class SpotifyContextObject(BaseModel):
    type: Literal["artist", "playlist", "album", "show"]
    href: str
    uri: str

    external_urls: SpotifyExternalUrls


class SpotifyPlaybackState(BaseModel):
    context: SpotifyContextObject
    item: SpotifyTrackObject

    progress_ms: int
    is_playing: bool

    repeat_state: Literal["off", "track", "context"]
    shuffle_state: bool
    currently_playing_type: Literal["track", "episode", "ad", "unknown"]


class SpotifyQueue(BaseModel):
    currently_playing: Optional[SpotifyTrackObject]
    queue: List[SpotifyTrackObject]


class ApiStats(BaseModel):

    total_requests: int
    total_listened: int

    song_request_timestamps: List[datetime.datetime]
