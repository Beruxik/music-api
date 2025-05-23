import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

sys.path.append("..")

from app.routers import preferences, songs

app = FastAPI()

app.mount("/url", StaticFiles(directory="static"), name="static")
app.include_router(songs.router)
app.include_router(preferences.router)
