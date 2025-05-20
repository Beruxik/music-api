import sys

from fastapi import FastAPI

sys.path.append("..")

from app.routers import songs

app = FastAPI()

app.include_router(songs.router)
