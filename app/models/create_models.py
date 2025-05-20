import sys

sys.path.append("..")

from sqlmodel import create_engine

from app.config import setup_logger
from app.models import MusicBase

engine = create_engine("sqlite:///music.db", echo=True)
logger = setup_logger(__name__)


def create_models() -> None:
    # Create the models
    MusicBase.metadata.create_all(engine)


if __name__ == "__main__":
    create_models()
    logger.info("Models created successfully.")
