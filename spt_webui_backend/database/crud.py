from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session
import sqlalchemy as sa

from spt_webui_backend.database import models
from spt_webui_backend import schemas


def create_user(db: Session, user: models.User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_discord_id(db: Session, discord_id: int) -> Optional[models.User]:
    return db.query(models.User).where(models.User.discord_user_id == discord_id).first()


def create_user_if_not_exists(db: Session, user: models.User):
    existing_user = get_user_by_discord_id(db, user.discord_user_id)

    if existing_user:
        if existing_user.discord_display_name != user.discord_display_name:
            db.execute(
                sa.update(models.User),
                [{"id": existing_user.id, "discord_display_name": user.discord_display_name}]
            )
            db.refresh(existing_user)

        return existing_user

    return create_user(db, user)


def get_user_by_id(db: Session, user_id: int):
    return db.get(models.User, user_id)


def get_artist_by_spotify_id(db: Session, spotify_id: str) -> Optional[models.RequestedSpotifySongArtist]:
    return db.execute(sa.select(models.RequestedSpotifySongArtist).where(models.RequestedSpotifySongArtist.spotify_id == spotify_id)).scalar()


def add_artists_for_song_if_not_exists(db: Session, spotify_track: schemas.SpotifyTrackObject, requested_song: Optional[models.RequestedSpotifySong] = None) -> List[models.RequestedSpotifySongArtist]:
    artists: List[models.RequestedSpotifySongArtist] = []
    for artist in spotify_track.artists:
        existing = get_artist_by_spotify_id(db, artist.id)
        if existing:
            artists.append(existing)

            existing.spotify_requested_songs.add(requested_song)
            db.commit()
            continue

        requested_artist = models.RequestedSpotifySongArtist(
            spotify_name=artist.name,
            spotify_id=artist.id,
            spotify_requested_songs={requested_song}
        )

        db.add(requested_artist)
        db.commit()
        db.refresh(requested_artist)
        artists.append(requested_artist)

    return artists


def get_spotify_requested_song_by_spotify_id(
        db: Session,
        spotify_id: str
) -> Optional[models.RequestedSpotifySong]:
    return db.execute(sa.select(models.RequestedSpotifySong).where(models.RequestedSpotifySong.spotify_id == spotify_id)).scalar()


def add_requested_song_if_not_exists(
        db: Session,
        spotify_track: schemas.SpotifyTrackObject,
) -> models.RequestedSpotifySong:

    existing = db.execute(
        sa.select(models.RequestedSpotifySong).where(models.RequestedSpotifySong.spotify_id == spotify_track.id)
    ).scalar()

    if existing:
        return existing

    requested_song = models.RequestedSpotifySong(
        spotify_name=spotify_track.name,
        spotify_id=spotify_track.id,
        spotify_large_image_link=spotify_track.album.images[0].url,
        spotify_small_image_link=spotify_track.album.images[-1].url,
    )

    db.add(requested_song)
    db.commit()
    db.refresh(requested_song)
    return requested_song



def add_song_request(db: Session, spotify_track: schemas.SpotifyTrackObject, user: models.User):
    requested_song = add_requested_song_if_not_exists(db, spotify_track)
    artists = add_artists_for_song_if_not_exists(db, spotify_track, requested_song)

    song_request = models.SongRequest(
        requested_song=requested_song,
        user=user,
        timestamp=datetime.now()
    )

    db.add(song_request)
    db.commit()
    db.refresh(song_request)
    return song_request




def get_stats(db: Session) -> schemas.ApiStats:
    total_requests = db.execute(sa.select(sa.func.count(models.RequestedSpotifySongArtist.id))).scalar()

    return schemas.ApiStats.model_validate({
        'total_requests': total_requests,
    })

