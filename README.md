# Music API 🎵

A FastAPI-based music management system that allows you to organize, categorize, and serve music files with preference-based recommendations.

## Features

- 🎵 **Song Management**: Store and organize music files with metadata (title, artist, file path)
- 🎸 **Genre Classification**: Automatic genre detection from folder structure
- 📋 **User Preferences**: Create custom playlists based on genre preferences
- 🔍 **Smart Recommendations**: Get songs based on your preferences
- 🎲 **Random Discovery**: Discover random songs from your collection
- 🚀 **RESTful API**: Full REST API with automatic OpenAPI documentation

## Project Structure

```
music-api/
├── app/
│   ├── config/          # Configuration and logging setup
│   ├── database/        # Database connection and session management
│   ├── models/          # SQLModel database models and table definitions
│   ├── routers/         # FastAPI route handlers
│   ├── services/        # Business logic and data processing
│   ├── static/music/    # Music file storage organized by genre
│   └── main.py          # FastAPI application entry point
├── pyproject.toml       # Project dependencies and configuration
├── uv.lock             # Dependency lock file
└── README.md           # This documentation
```

## Installation

### Prerequisites

- Python 3.13+
- `uv` package manager

### Setup with uv

1. **Clone the repository**:
```bash
git clone https://github.com/Beruxik/music-api
cd music-api
```

2. **Install dependencies using uv**:
```bash
uv sync
```

3. **Activate the virtual environment**:
```bash
source .venv/bin/activate
```

4. **Initialize the database**:
```bash
cd app/models
uv run create_models.py
```

5. **Populate with data**:
```bash
cd ../services
uv run insert_data.py
```

## Running the Application

### Development Server

Start the FastAPI development server:

```bash
cd music-api/app
uv run fastapi dev
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Documentation

### Songs Endpoints

#### Get Random Songs
```http
GET /songs/random?limit=10
```

**Parameters:**
- `limit` (optional): Number of songs to return (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Levels",
    "artist": "Avicii",
    "file_path": "static/music/electronic/Avicii - Levels.webm"
  }
]
```

#### Get Songs by Preference
```http
GET /songs/{preference_id}?limit=10&offset=0
```

**Parameters:**
- `preference_id`: ID of the preference
- `limit` (optional): Number of songs to return (default: 10)
- `offset` (optional): Number of songs to skip (default: 0)

### Preferences Endpoints

#### List All Preferences
```http
GET /preferences
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "My Rock Collection",
    "genres": ["rock", "metal"]
  }
]
```

#### Create a New Preference
```http
POST /preferences
```

**Request Body:**
```json
{
  "title": "My Electronic Mix",
  "genres": ["electronic", "pop"]
}
```

#### Update a Preference
```http
PATCH /preferences/{preference_id}
```

**Request Body:**
```json
{
  "title": "Updated Playlist Name"
}
```

#### Delete a Preference
```http
DELETE /preferences/{preference_id}
```

## Database Schema

The application uses SQLite with the following main models:

### Song
- `id`: Primary key
- `title`: Song title
- `artist`: Artist name
- `file_path`: Path to the music file

### Genre
- `id`: Primary key
- `name`: Genre name (unique)

### Preference
- `id`: Primary key
- `title`: Preference/playlist name

### Relationships
- **Songs ↔ Genres**: Many-to-many relationship via `SongGenreLink`
- **Preferences ↔ Genres**: Many-to-many relationship via `PreferenceGenreLink`

## Adding Music Files

1. **Organize your music** in the `app/static/music/` directory by genre:
```
app/static/music/
├── electronic/
│   ├── Avicii - Levels.webm
│   └── Avicii - Wake Me Up.webm
├── rock/
│   ├── AC⧸DC - Thunderstruck.webm
│   └── Nirvana - Smells Like Teen Spirit.webm
└── pop/
    └── Taylor Swift - Shake It Off.webm
```

2. **Run the data import script**:
```bash
cd app/services
python insert_data.py
```

The script will:
- Automatically detect genres from folder names
- Extract artist and title from filenames (format: "Artist - Title.extension")
- Create database entries for songs and genres
- Handle duplicate prevention

## Example Usage

### Using curl

**Create a preference:**
```bash
curl -X POST "http://localhost:8000/preferences" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Workout Playlist",
    "genres": ["electronic", "rock"]
  }'
```

**Get songs for a preference:**
```bash
curl "http://localhost:8000/songs/1?limit=5"
```

**Get random songs:**
```bash
curl "http://localhost:8000/songs/random?limit=3"
```

### Using Python requests

```python
import requests

# Create a preference
response = requests.post(
    "http://localhost:8000/preferences",
    json={
        "title": "Chill Mix",
        "genres": ["pop", "electronic"]
    }
)
preference = response.json()

# Get songs for this preference
songs_response = requests.get(
    f"http://localhost:8000/songs/{preference['id']}?limit=10"
)
songs = songs_response.json()
```

## Configuration

### Environment Variables

You can configure the application using environment variables:

- `DATABASE_URL`: Database connection string (default: `sqlite:///music.db`)
- `DEBUG`: Enable debug mode (default: `False`)

### Logging

The application uses structured logging. Logs include:
- Request/response information
- Database operations
- Error tracking

## Development

### Code Quality

The project uses:
- **Ruff**: For linting and code formatting
- **Type hints**: Full type annotation support
- **SQLModel**: For type-safe database operations

### Running Tests

```bash
# Run linting
uv run ruff check app/

# Format code
uv run ruff format app/
```

## Troubleshooting

### Common Issues

1. **Database not found**: Make sure to run `python app/models/create_models.py` first
2. **Music files not loading**: Check that files are in the correct directory structure
3. **Permission errors**: Ensure the application has read access to the music directory

### Logs

Check the application logs for detailed error information. Logs are printed to stdout in JSON format.

## License

This project is licensed under the MIT License.
