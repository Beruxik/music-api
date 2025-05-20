import sys
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

sys.path.append("..")
from app.models import MusicBase, PreferenceGenreLink, SongPreferenceLink

if TYPE_CHECKING:
    from app.models import Genre, Song


class Preference(MusicBase, table=True):
    """
    A model representing a preference in the music database.
    """

    id: int = Field(default=None, primary_key=True)
    title: str
    songs: list["Song"] = Relationship(
        back_populates="preferences",
        link_model=SongPreferenceLink,
    )
    genres: list["Genre"] = Relationship(
        back_populates="preferences",
        link_model=PreferenceGenreLink,
    )
