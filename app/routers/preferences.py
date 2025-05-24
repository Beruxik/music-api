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
        from_attributes = True


class PreferenceWithGenresResponse(PreferenceResponse):
    genres: list[str]  # List of genre names associated with this preference


SessionDep = Annotated[Session, Depends(get_session)]
logger = setup_logger(__name__)

router = APIRouter(
    prefix="/preferences",
    tags=["preferences"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def read_preferences(
    session: SessionDep,
) -> list[PreferenceWithGenresResponse]:
    """
    Retrieve all preferences.
    """
    preferences = session.exec(select(Preference)).all()

    preferences_with_genres = [
        {
            "id": preference.id,
            "title": preference.title,
            "genres": [genres.name for genres in preference.genres],
        }
        for preference in preferences
    ]

    return preferences_with_genres  # noqa: RET504


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


@router.delete("/{preference_id}")
def delete_preference(
    preference_id: int,
    session: SessionDep,
) -> None:
    """
    Delete a preference by ID.
    """
    preference = session.get(Preference, preference_id)
    if not preference:
        raise HTTPException(status_code=404, detail="Preference not found")

    session.delete(preference)
    session.commit()
    return {"ok": True}
