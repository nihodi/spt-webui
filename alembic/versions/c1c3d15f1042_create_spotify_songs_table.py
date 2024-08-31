"""create requested_spotify_songs table

Revision ID: c1c3d15f1042
Revises: 620b6a364273
Create Date: 2024-08-25 14:22:17.340285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c1c3d15f1042'
down_revision: Union[str, None] = '620b6a364273'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "requested_spotify_songs_artists",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("spotify_id", sa.String(50), nullable=False, unique=True),
        sa.Column("spotify_name", sa.Unicode(255), nullable=False),
    )

    op.create_table(
        "requested_spotify_songs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("spotify_id", sa.String(50), nullable=False, unique=True),
        sa.Column("spotify_name", sa.Unicode(255), nullable=False),
        sa.Column("spotify_large_image_link", sa.String(255), nullable=False),
        sa.Column("spotify_small_image_link", sa.String(255), nullable=False),
    )

    op.create_table(
        "requested_spotify_songs_artist_connections",
        sa.Column(
            "requested_spotify_song_id",
            sa.Integer,
            sa.ForeignKey("requested_spotify_songs.id"),
            primary_key=True,
        ),
        sa.Column(
            "requested_spotify_songs_artists_id",
            sa.Integer,
            sa.ForeignKey("requested_spotify_songs_artists.id"),
            primary_key=True,
        ),
    )

    op.create_table(
        "song_requests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("requested_song_id", sa.Integer, sa.ForeignKey("requested_spotify_songs.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("timestamp", sa.DateTime, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("song_requests")
    op.drop_table("requested_spotify_songs_artist_connections")
    op.drop_table("requested_spotify_songs")
    op.drop_table("requested_spotify_songs_artists")
