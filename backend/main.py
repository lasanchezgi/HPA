from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from src.delivery.api.router import api_router
from src.delivery.middleware import ExceptionHandlerMiddleware
from src.delivery.schemas.common import HealthResponse

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if settings.ENVIRONMENT == "development":
        from src.infrastructure.database.session import engine
        from src.infrastructure.database.models.base import Base
        # Import all models so metadata is populated
        import src.infrastructure.database.models.user_model  # noqa: F401
        import src.infrastructure.database.models.habit_model  # noqa: F401
        import src.infrastructure.database.models.habit_log_model  # noqa: F401
        import src.infrastructure.database.models.catalogue_model  # noqa: F401

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Habit Power API",
    version="1.0.0",
    description="Track habits, build streaks, earn rewards.",
    lifespan=lifespan,
)

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENVIRONMENT == "development" else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
