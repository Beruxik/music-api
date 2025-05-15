import sys

sys.path.append("..")

from sqlalchemy import create_engine

from app.models import MusicBase

engine = create_engine("sqlite:///music.db", echo=True)


def create_models() -> None:
    # Create the models
    MusicBase.metadata.create_all(engine)


if __name__ == "__main__":
    create_models()
    print("Models created successfully.")
