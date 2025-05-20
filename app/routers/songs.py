from fastapi import APIRouter
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.config import setup_logger
from app.models import Song

router = APIRouter(
    prefix="/songs",
    tags=["songs"],
    responses={404: {"description": "Not found"}},
)

engine = create_engine("sqlite:///music.db", echo=True)
logger = setup_logger(__name__)


@router.get("/random")
async def get_random_songs() -> dict:
    """
    Get a random song from the database.
    """
    songs = []
    # Assuming you have a function to get a random song
    with Session(engine) as session:
        stmt = select(Song)
        for row in session.execute(stmt):
            song = [r for r in row]
            songs.append(song)
    logger.info(f"Random songs: {songs}")

    return {"song": "test"}
