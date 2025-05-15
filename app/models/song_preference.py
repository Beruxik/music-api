import sys

from sqlalchemy import Column, ForeignKey, Integer, Table

sys.path.append("..")
from app.models import MusicBase

song_preference: Table = Table(
    "song_preference",
    MusicBase.metadata,
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("preference_id", Integer, ForeignKey("preferences.id"), primary_key=True),
)
