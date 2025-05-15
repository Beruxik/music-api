import sys
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

sys.path.append("..")
from app.models import Genre, MusicBase, Preference, song_genre, song_preference

if TYPE_CHECKING:
    from app.models import Genre, Preference


class Song(MusicBase):
    __tablename__: str = "songs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    preferences: Mapped[list["Preference"]] = relationship(
        secondary=song_preference,
        back_populates="songs",
    )
    genres: Mapped[list["Genre"]] = relationship(
        secondary=song_genre,
        back_populates="songs",
    )
