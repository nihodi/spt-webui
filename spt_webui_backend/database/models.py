import datetime
from typing import List, Set

import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.orm import Mapped, mapped_column

BaseModel = sa.orm.DeclarativeBase


class Base(BaseModel):
    metadata = sa.MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)

    discord_user_id: Mapped[int] = mapped_column(sa.BigInteger, unique=True)
    discord_display_name: Mapped[str] = mapped_column(sa.Unicode(255))

spotify_songs_artists_association_table = sa.Table(
    "requested_spotify_songs_artist_connections",
    Base.metadata,
    sa.Column("requested_spotify_song_id", sa.ForeignKey("requested_spotify_songs.id"), primary_key=True),
    sa.Column("requested_spotify_songs_artists_id", sa.ForeignKey("requested_spotify_songs_artists.id"), primary_key=True),
)


class RequestedSpotifySong(Base):
    __tablename__ = 'requested_spotify_songs'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    spotify_id: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)

    spotify_name: Mapped[str] = mapped_column(sa.Unicode(255), nullable=False)

    spotify_large_image_link: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    spotify_small_image_link: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    length_ms: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    explicit: Mapped[bool] = mapped_column(sa.Boolean, nullable=False)

    spotify_artists: Mapped[List["RequestedSpotifySongArtist"]] = sa.orm.relationship(
        secondary=spotify_songs_artists_association_table,
        back_populates="spotify_requested_songs",
    )


class RequestedSpotifySongArtist(Base):
    __tablename__ = "requested_spotify_songs_artists"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    spotify_id: Mapped[str] = mapped_column(sa.String(50), unique=True, nullable=False)
    spotify_name: Mapped[str] = mapped_column(sa.Unicode(255), nullable=False)

    spotify_requested_songs: Mapped[Set[RequestedSpotifySong]] = sa.orm.relationship(
        secondary=spotify_songs_artists_association_table,
        back_populates="spotify_artists",
    )


class SongRequest(Base):
    __tablename__ = 'song_requests'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)

    timestamp: Mapped[datetime.datetime] = mapped_column(sa.DateTime, nullable=False)

    requested_song_id: Mapped[int] = mapped_column(
        sa.ForeignKey(RequestedSpotifySong.id, name="fk_song_requests_requested_song_id_requested_spotify_songs")
    )


    user_id: Mapped[int] = mapped_column(sa.ForeignKey(User.id, name="fk_song_requests_user_id_users"))

    user: Mapped[User] = sa.orm.relationship(
        User,
        foreign_keys=user_id,
    )

    requested_song: Mapped[RequestedSpotifySong] = sa.orm.relationship(
        RequestedSpotifySong,
        foreign_keys=requested_song_id,
    )
