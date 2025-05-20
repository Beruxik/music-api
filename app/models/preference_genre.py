import sys

sys.path.append("..")

from sqlmodel import Field

from app.models import MusicBase


class PreferenceGenreLink(MusicBase, table=True):
    """
    A model representing the relationship between a preference and a genre.
    This model is used to link preferences to genres in the database.
    """

    preference_id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key="preference.id",
    )
    genre_id: int | None = Field(
        default=None,
        primary_key=True,
        foreign_key="genre.id",
    )
