import random
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.config import setup_logger
from app.database import get_session
from app.models import Song

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
