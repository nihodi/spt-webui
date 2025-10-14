"""add requested_spotify_songs_artists image columns, and populate data

Revision ID: 5e12b45366ad
Revises: d53e6e46f03a
Create Date: 2024-09-24 20:05:58.684749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from spt_webui_backend import spotify
from spt_webui_backend.database import models

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

# revision identifiers, used by Alembic.
revision: str = '5e12b45366ad'
down_revision: Union[str, None] = 'd53e6e46f03a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("requested_spotify_songs_artists", sa.Column("spotify_large_image_link", sa.String(255), nullable=True))
    op.add_column("requested_spotify_songs_artists", sa.Column("spotify_small_image_link", sa.String(255), nullable=True))

    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    requested_artists = session.execute(sa.select(models.RequestedSpotifySongArtist)).scalars()
    spotify_instance = spotify.get_spotify_instance()

    for songs in batched(requested_artists, 50):
        for artist in spotify_instance.get_artists(ids=[song.spotify_id for song in songs]):
            try:
                large = artist.images[0].url
            except IndexError:
                large = None

            try:
                small = artist.images[-1].url
            except IndexError:
                small = None

            session.execute(sa.update(models.RequestedSpotifySongArtist)
                            .where(models.RequestedSpotifySongArtist.spotify_id == artist.id)
                            .values(spotify_large_image_link=large, spotify_small_image_link=small))




def downgrade() -> None:
    op.drop_column("requested_spotify_songs_artists", "spotify_large_image_link")
    op.drop_column("requested_spotify_songs_artists", "spotify_small_image_link")