import sys

from sqlmodel import Field

sys.path.append("..")
from app.models import MusicBase


class SongGenreLink(MusicBase, table=True):
    """
    A model representing the relationship between a song and a genre.
    This model is used to link songs to genres in the database.
    """

    song_id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key="song.id",
    )
    genre_id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key="genre.id",
    )
