import sys

from sqlalchemy.orm import DeclarativeBase

sys.path.append("..")


class MusicBase(DeclarativeBase):
    """
    Base class for SQLAlchemy models in the music database.
    This class inherits from DeclarativeBase,
    which is a base class for declarative class definitions.
    """


from app.models.genre import Genre  # noqa: E402
from app.models.preference import Preference  # noqa: E402
from app.models.preference_genre import preference_genre  # noqa: E402
from app.models.song import Song  # noqa: E402
from app.models.song_genre import song_genre  # noqa: E402
from app.models.song_preference import song_preference  # noqa: E402

__all__ = [
    "Genre",
    "MusicBase",
    "Preference",
    "Song",
    "preference_genre",
    "song_genre",
    "song_preference",
]
