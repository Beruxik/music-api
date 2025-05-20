import sys
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models import MusicBase, PreferenceGenreLink, SongGenreLink

sys.path.append("..")

if TYPE_CHECKING:
    from app.models import Preference, Song


class Genre(MusicBase, table=True):
    """
    A model representing a genre in the music database.
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    songs: list["Song"] = Relationship(
        back_populates="genres",
        link_model=SongGenreLink,
    )
    preferences: list["Preference"] = Relationship(
        back_populates="genres",
        link_model=PreferenceGenreLink,
    )
