import datetime
import fastapi
import json
import requests
import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import APIRouter, Query
from typing import Annotated

from spt_webui_backend import spotify, schemas, database, security
from spt_webui_backend.database import crud
from spt_webui_backend.environment import ENVIRONMENT

router = APIRouter(tags=["playback"])


@router.get(
    "/playback/state",
    responses={
        200: {
            "model": schemas.SpotifyPlaybackState
        },
        204: {
            "model": None,
            "description": "Playback not available or active"
        }
    }
)
def get_spotify_playback_state(
        spotify_instance: spotify.Spotify = fastapi.Depends(spotify.get_spotify_instance)
):
    state = spotify_instance.get_playback_state()
    if state is None:
        return fastapi.Response(status_code=204)
    return state


@router.post(
    "/playback/queue",
    responses={
        200: {"model": None},
        401: security.HTTP_401,
        409: {
            "model": None,
            "description": "Song is already present in the queue."
        }
    }
)
def add_spotify_queue_item(
        url: Annotated[
            str,
            Query(
                pattern=r"https://open.spotify.com/track/[a-zA-Z0-9]+",
                title="Spotify song URL",
                description="A link to a Spotify song.",
                openapi_examples={
                    "たぶん by YOASOBI": {
                        "value": "https://open.spotify.com/track/398dL22bDbKbAmiOnPaq7o",
                        "description": "Spotify song URL for たぶん by YOASOBI.",
                    }
                }
            )
        ],
        background_tasks: fastapi.BackgroundTasks,
        db: sa.orm.Session = fastapi.Depends(database.get_db),
        user: database.models.User = fastapi.Depends(security.get_current_user),
        spotify_instance: spotify.Spotify = fastapi.Depends(spotify.get_spotify_instance)
):
    track_uri = f"spotify:track:{spotify.get_track_id_from_shared_url(url)}"

    if spotify_instance.track_is_in_queue(track_uri):
        raise fastapi.HTTPException(fastapi.status.HTTP_409_CONFLICT,
                                    detail="Song is already present in the queue or is already playing.")

    spotify_track = spotify_instance.add_track_to_queue(f"{track_uri}")
    print(f"User {user.discord_display_name} requested the song {spotify_track.name}")

    # background task
    def add_track_to_playlist():
        if not crud.get_spotify_requested_song_by_spotify_id(db, spotify_track.id):
            if ENVIRONMENT.spotify_playlist_id:
                spotify_instance.add_tracks_to_playlist(ENVIRONMENT.spotify_playlist_id, [spotify_track.uri])

        crud.add_song_request(db, spotify_track, user)

        if not ENVIRONMENT.discord_webhook_url:
            return

        # send discord webhook. looks scary, it really isn't.
        artists = ", ".join([artist.name for artist in spotify_track.artists])
        data = json.dumps(
            {
                "content": "",
                "embeds": [
                    {
                        "title": f"{artists} - {spotify_track.name}",
                        "description": "Song requested!\n\nRequest your own songs [here](https://niklas.dietzel.no/spt-webui/)!",
                        "url": spotify_track.external_urls.spotify,
                        "color": 5814783,
                        "footer": {
                            "text": "spt-webui webhook"
                        },
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                        "image": {
                            "url": spotify_track.album.images[0].url,
                        },
                        "thumbnail": {
                            "url": "https://storage.googleapis.com/pr-newsroom-wp/1/2023/05/Spotify_Primary_Logo_RGB_Green.png"
                        }
                    }
                ],
                "username": "spt-webui",
                "attachments": []
            }
        )

        resp = requests.post(
            ENVIRONMENT.discord_webhook_url + "?wait=true",
            data=data,
            headers={"Content-Type": "application/json"},
        )

        resp.raise_for_status()

    background_tasks.add_task(add_track_to_playlist)
    return spotify_track


@router.get("/playback/queue")
def get_spotify_playback_queue(
        spotify_instance: spotify.Spotify = fastapi.Depends(spotify.get_spotify_instance)

):
    return spotify_instance.get_playback_queue()


@router.get("/stats", response_model=schemas.ApiStats)
def get_stats(
        db: sa.orm.Session = fastapi.Depends(database.get_db)
):
    return crud.get_stats(db)
