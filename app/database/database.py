from collections.abc import Generator

from sqlmodel import Session, create_engine

sqlite_file_name = "music.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session
