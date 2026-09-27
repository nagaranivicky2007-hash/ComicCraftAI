from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi.staticfiles import (
    StaticFiles
)

from app.config import (
    BASE_DIR,
    get_settings
)

from app.routes import router

from app.utils import (
    ensure_directories
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    ensure_directories(
        BASE_DIR / "static" / "panels",
        BASE_DIR / "static" / "exports"
    )

    yield


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    description=(
        "AI Comic Story Creator using "
        "Gemini and Stable Diffusion-compatible "
        "image generation."
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(
        directory=str(
            BASE_DIR / "static"
        )
    ),
    name="static"
)


app.include_router(router)