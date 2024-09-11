"""add requested songs to spotify playlist (if set)

Revision ID: 7d36833c6b32
Revises: c1c3d15f1042
Create Date: 2024-09-11 18:29:12.673155

not really a database revision, but I'm using this "framework" because it's convenient

"""

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

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.orm

import spt_webui_backend.spotify as spotify
from spt_webui_backend.database import models
from spt_webui_backend.environment import ENVIRONMENT

# revision identifiers, used by Alembic.
revision: str = '7d36833c6b32'
down_revision: Union[str, None] = 'c1c3d15f1042'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if ENVIRONMENT.spotify_playlist_id is None:
        print("Skipping migration due to SPOTIFY_PLAYLIST_ID not being set.")
        return

    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    song_ids = session.execute(sa.select(models.RequestedSpotifySong.spotify_id)).scalars()
    song_ids = [f"spotify:track:{song_id}" for song_id in song_ids]
    song_ids = batched(song_ids, 100)

    spotify_instance = spotify.get_spotify_instance()

    for batch in song_ids:
        spotify_instance.add_tracks_to_playlist(ENVIRONMENT.spotify_playlist_id, batch)


def downgrade() -> None:
    print("WARN: Downgrading '7d36833c6b32 add requested songs to spotify playlist (if set)' currently does nothing!")
