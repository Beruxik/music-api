import sys

from sqlmodel import SQLModel

sys.path.append("..")


class MusicBase(SQLModel):
    """
    Base class for SQLAlchemy models in the music database.
    This class inherits from DeclarativeBase,
    which is a base class for declarative class definitions.
    """


from app.models.song_genre import SongGenreLink  # noqa: E402, I001
from app.models.preference_genre import PreferenceGenreLink  # noqa: E402
from app.models.song_preference import SongPreferenceLink  # noqa: E402
from app.models.genre import Genre  # noqa: E402
from app.models.preference import Preference  # noqa: E402
from app.models.song import Song  # noqa: E402

__all__ = [
    "Genre",
    "MusicBase",
    "Preference",
    "PreferenceGenreLink",
    "Song",
    "SongGenreLink",
    "SongPreferenceLink",
]
