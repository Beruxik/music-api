from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.config import setup_logger
from app.database import get_session
from app.models import Genre, MusicBase, Preference


# Request models
class PreferenceCreate(MusicBase):
    title: str
    genres: list[str]  # List of genre IDs to associate with this preference


# Response models
class PreferenceResponse(MusicBase):
    id: int
    title: str

    class Config:
        orm_mode = True


SessionDep = Annotated[Session, Depends(get_session)]
logger = setup_logger(__name__)

router = APIRouter(
    prefix="/preferences",
    tags=["preferences"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
def create_preferences(
    preference_data: PreferenceCreate,
    session: SessionDep,
) -> Preference:
    """
    Create a new preference.
    """
    new_preference = Preference(title=preference_data.title)
    session.add(new_preference)

    for genre_name in preference_data.genres:
        genre = session.exec(select(Genre).where(Genre.name == genre_name)).first()
        if not genre:
            session.rollback()
            raise HTTPException(status_code=404, detail=f"Genre {genre_name} not found")
        new_preference.genres.append(genre)

    session.commit()
    session.refresh(new_preference)
    return new_preference
