import sys

from fastapi import FastAPI

sys.path.append("..")

from app.routers import preferences, songs

app = FastAPI()

app.include_router(songs.router)
app.include_router(preferences.router)
