import pathlib
import re
import sys

from sqlmodel import Session, create_engine, select

sys.path.append("..")

from app.config import setup_logger
from app.models import Genre, Song

logger = setup_logger(__name__)


def remove_enclosed_text(text: str, opening_chars: str, closing_chars: str) -> str:
    """
    Removes text enclosed between any characters from opening_chars and their
    corresponding characters in closing_chars.

    Args:
        text: The input string
        opening_chars: String of opening delimiter characters (e.g., "([")
        closing_chars: String of closing delimiter characters (e.g., ")]")

    Returns:
        String with enclosed content removed
    """
    result = text

    # Process each opening/closing character pair
    for i, open_char in enumerate(opening_chars):
        if i < len(closing_chars):
            close_char = closing_chars[i]
            # Escape special regex characters
            open_escaped = re.escape(open_char)
            close_escaped = re.escape(close_char)
            # Create pattern that matches content between this specific pair
            pattern = f"{open_escaped}[^{close_escaped}]*{close_escaped}"
            # Remove matching content
            result = re.sub(pattern, "", result)

    return result


def insert_data(session: Session) -> None:
    """
    Insert sample data into the database.
    """
    # Cache genres to avoid duplicate queries and inserts
    genre_cache = {}
    song_cache = {}

    for directory in pathlib.Path("static/music").iterdir():
        for file in directory.glob("*.webm"):
            genre_name = file.parent.name.split("/")[-1]
            file_path = str(file)  # Get file_path early to use for lookup

            # Check if genre exists in our cache or fetch/create it
            if genre_name not in genre_cache:
                # Try to find the genre in the database
                existing_genre = session.exec(
                    select(Genre).where(Genre.name == genre_name),
                ).first()
                if existing_genre:
                    # Use existing genre
                    genre_cache[genre_name] = existing_genre
                else:
                    # Create new genre
                    new_genre = Genre(name=genre_name)
                    session.add(new_genre)
                    session.flush()  # Get ID before using the relation
                    genre_cache[genre_name] = new_genre

            # Check if song already exists by file path
            if file_path not in song_cache:
                existing_song = session.exec(
                    select(Song).where(Song.file_path == file_path),
                ).first()
                if existing_song:
                    # Use existing song
                    song_cache[file_path] = existing_song
                    continue  # Skip to next file

                # Process new song
                file_name = remove_enclosed_text(file.stem, "([", ")]")
                title = (
                    file_name.split(" - ")[-1].strip()
                    if " - " in file_name
                    else file_name
                )
                artist = (
                    file_name.split(" - ")[0].strip()
                    if " - " in file_name
                    else "Unknown Artist"
                )

                # Create new song
                new_song = Song(
                    title=title,
                    artist=artist,
                    file_path=file_path,
                )

                # Add genre to song
                new_song.genres.append(genre_cache[genre_name])
                session.add(new_song)
                session.flush()  # Get ID before using the relation
                song_cache[file_path] = new_song


if __name__ == "__main__":
    engine = create_engine("sqlite:///music.db")
    # Create a new session
    session: Session = Session(engine)

    try:
        # Call the insert_data function
        insert_data(session)
        session.commit()
        logger.info("Successfully inserted data into database")
    except Exception:
        session.rollback()
        logger.exception("Found an error")
        raise
    finally:
        # Close the session
        session.close()
