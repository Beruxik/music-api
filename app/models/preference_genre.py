import sys

sys.path.append("..")

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models import MusicBase

preference_genre: Table = Table(
    "preference_genre",
    MusicBase.metadata,
    Column("preference_id", Integer, ForeignKey("preferences.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)
