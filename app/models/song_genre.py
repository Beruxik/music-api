import sys

sys.path.append("..")

from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models import MusicBase

song_genre: Table = Table(
    "song_genre",
    MusicBase.metadata,
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)
