import random
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.config import setup_logger
from app.database import get_session
from app.models import MusicBase, PreferenceGenreLink, Song, SongGenreLink


class SongResponse(MusicBase):
    id: int
    title: str
    artist: str
    file_path: str
    genre: str

    class Config:
        from_attributes = True


SessionDep = Annotated[Session, Depends(get_session)]
logger = setup_logger(__name__)

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/random")
def read_songs(
    session: SessionDep,
    limit: int = 10,
) -> list[SongResponse]:
    songs = session.exec(select(Song)).all()
    songs_with_genres = [
        {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "file_path": song.file_path,
            "genre": next(genres.name for genres in song.genres),
        }
        for song in songs
    ]
    return random.sample(songs_with_genres, min(limit, len(songs)))


@router.get("/{preference_id}")
def read_songs_by_preference(
    preference_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,
) -> list[SongResponse]:
    songs = session.exec(
        select(Song)
        .join(SongGenreLink, SongGenreLink.song_id == Song.id)
        .join(
            PreferenceGenreLink,
            PreferenceGenreLink.genre_id == SongGenreLink.genre_id,
        )
        .where(PreferenceGenreLink.preference_id == preference_id)
        .where(SongGenreLink.genre_id == PreferenceGenreLink.genre_id)
        .where(SongGenreLink.song_id == Song.id)
        .offset(offset)
        .limit(limit),
    ).all()

    songs_with_genres = [
        {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "file_path": song.file_path,
            "genre": next(genres.name for genres in song.genres),
        }
        for song in songs
    ]

    return songs_with_genres  # noqa: RET504
