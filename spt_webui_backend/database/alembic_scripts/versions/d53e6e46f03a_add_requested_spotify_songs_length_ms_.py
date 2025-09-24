"""add requested_spotify_songs.length_ms .explicit column, and populate data

Revision ID: d53e6e46f03a
Revises: 7d36833c6b32
Create Date: 2024-09-24 16:16:07.046979

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlalchemy.orm
from alembic import op

try:
    from itertools import batched
except ImportError:
    from itertools import islice


    # grabbed from for python 3.11 compatability.
    # TODO: remove when debian 13 releases...
    # https://docs.python.org/3/library/itertools.html#itertools.batched

    def batched(iterable, n):
        # batched('ABCDEFG', 3) → ABC DEF G
        if n < 1:
            raise ValueError('n must be at least one')
        iterator = iter(iterable)
        while batch := tuple(islice(iterator, n)):
            yield batch

from spt_webui_backend import spotify
from spt_webui_backend.database import models

# revision identifiers, used by Alembic.
revision: str = 'd53e6e46f03a'
down_revision: Union[str, None] = '7d36833c6b32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("requested_spotify_songs", sa.Column("length_ms", sa.Integer(), nullable=True))
    op.add_column("requested_spotify_songs", sa.Column("explicit", sa.Boolean(), nullable=True))

    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    requested_songs = session.execute(sa.select(models.RequestedSpotifySong)).scalars()
    spotify_instance = spotify.get_spotify_instance()

    for songs in batched(requested_songs, 50):
        for track in spotify_instance.get_tracks(ids=[song.spotify_id for song in songs]):
            session.execute(sa.update(models.RequestedSpotifySong)
                            .where(models.RequestedSpotifySong.spotify_id == track.id)
                            .values(explicit=track.explicit, length_ms=track.duration_ms))

    op.alter_column("requested_spotify_songs", "length_ms", nullable=False, type_=sa.Integer)
    op.alter_column("requested_spotify_songs", "explicit", nullable=False, type_=sa.Boolean)


def downgrade() -> None:
    op.drop_column("requested_spotify_songs", "length_ms")
    op.drop_column("requested_spotify_songs", "explicit")
