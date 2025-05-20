import sys
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

sys.path.append("..")
from app.models import MusicBase, SongGenreLink, SongPreferenceLink

if TYPE_CHECKING:
    from app.models import Genre, Preference


class Song(MusicBase, table=True):
    """
    A model representing a song in the music database.
    """

    id: int = Field(default=None, primary_key=True)
    title: str
    artist: str
    file_path: str
    genres: list["Genre"] = Relationship(
        back_populates="songs",
        link_model=SongGenreLink,
    )
    preferences: list["Preference"] = Relationship(
        back_populates="songs",
        link_model=SongPreferenceLink,
    )
