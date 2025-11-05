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


class SpotifyImageObject(BaseModel):
    url: str
    width: int
    height: int


class SpotifySimplifiedArtistObject(BaseModel):
    href: str
    id: str
    uri: str

    name: str
    type: Literal["artist"]

    external_urls: SpotifyExternalUrls


class SpotifyArtistObject(SpotifySimplifiedArtistObject):
    class Followers(BaseModel):
        total: int

    followers: Followers
    genres: List[str]
    popularity: int

    images: List[SpotifyImageObject]


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

class QueueTrackObject(SpotifyTrackObject):
    queue_type: Literal["queue", "next_up"] = "next_up"

class SpotifyContextObject(BaseModel):
    type: Literal["artist", "playlist", "album", "show", "collection"]
    href: str
    uri: str

    external_urls: SpotifyExternalUrls


class SpotifyPlaybackState(BaseModel):
    context: Optional[SpotifyContextObject]
    item: SpotifyTrackObject

    progress_ms: int
    is_playing: bool

    repeat_state: Literal["off", "track", "context"]
    shuffle_state: bool
    currently_playing_type: Literal["track", "episode", "ad", "unknown"]


class SpotifyQueue(BaseModel):
    currently_playing: Optional[SpotifyTrackObject]
    queue: List[QueueTrackObject]


class DbSpotifyArtist(BaseModel):
    spotify_name: str
    spotify_id: str

    spotify_large_image_link: Optional[str]
    spotify_small_image_link: Optional[str]

    class Config:
        from_attributes = True


class DbSpotifySong(BaseModel):
    spotify_name: str
    spotify_id: str

    spotify_large_image_link: str
    spotify_small_image_link: str

    explicit: bool
    length_ms: int

    spotify_artists: List[DbSpotifyArtist]

    class Config:
        from_attributes = True


class ApiStats(BaseModel):
    total_requests: int
    total_ms_listened: int

    class DateRequestCount(BaseModel):
        date: datetime.date
        request_count: int

        class Config:
            from_attributes = True

    requests_grouped_by_date: List[DateRequestCount]

    class RequestedArtist(BaseModel):
        artist: DbSpotifyArtist
        request_count: int

    most_requested_artists: List[RequestedArtist]

    class RequestedSong(BaseModel):
        song: DbSpotifySong
        request_count: int

    most_requested_songs: List[RequestedSong]
