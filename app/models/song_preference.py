import sys

from sqlmodel import Field

sys.path.append("..")
from app.models import MusicBase


class SongPreferenceLink(MusicBase, table=True):
    """
    A model representing the relationship between a song and a preference.
    This model is used to link songs to preferences in the database.
    """

    song_id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key="song.id",
    )
    preference_id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key="preference.id",
    )
