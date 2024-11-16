from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ms_core import setup_app

from app import settings
from app.settings import db_url

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # Quit browser
    settings.driver.quit()

application = FastAPI(
    title="ShkoloMS",
    version="0.1.0",
    lifespan=lifespan
)

setup_app(
    application,
    db_url,
    Path("app") / "routers",
    ["app.models"]
)

# noinspection PyTypeChecker
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:application", port=8000, reload=True)
