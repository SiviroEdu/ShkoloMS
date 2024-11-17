import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ms_core import setup_app

from app import settings
from app.settings import db_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    # Quit browser
    # settings.driver.quit()
    await settings.session.close()

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

@application.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
