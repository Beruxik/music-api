import sys
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

sys.path.append("..")
from app.models import MusicBase, preference_genre, song_preference

if TYPE_CHECKING:
    from app.models import Genre, Song


class Preference(MusicBase):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    songs: Mapped[list["Song"]] = relationship(
        back_populates="preferences",
        secondary=song_preference,
    )
    genres: Mapped[list["Genre"]] = relationship(
        back_populates="preferences",
        secondary=preference_genre,
    )
