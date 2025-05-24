import random
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.config import setup_logger
from app.database import get_session
from app.models import PreferenceGenreLink, Song, SongGenreLink

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
) -> list[Song]:
    songs = session.exec(select(Song)).all()
    return random.sample(songs, limit)


@router.get("/{preference_id}")
def read_songs_by_preference(
    preference_id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=10)] = 10,
) -> list[Song]:
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
    return songs  # noqa: RET504
