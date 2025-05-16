import sys
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

sys.path.append("..")
from app.models import MusicBase, preference_genre, song_genre

if TYPE_CHECKING:
    from app.models import Preference, Song


class Genre(MusicBase):
    __tablename__: str = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    songs: Mapped[list["Song"]] = relationship(
        back_populates="genres",
        secondary=song_genre,
    )
    preferences: Mapped[list["Preference"]] = relationship(
        back_populates="genres",
        secondary=preference_genre,
    )
