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
        from sqlalchemy import func, select
        from sqlalchemy.ext.asyncio import AsyncSession

        from src.infrastructure.database.session import engine
        from src.infrastructure.database.models.base import Base
        import src.infrastructure.database.models.user_model  # noqa: F401
        import src.infrastructure.database.models.habit_model  # noqa: F401
        import src.infrastructure.database.models.habit_log_model  # noqa: F401
        import src.infrastructure.database.models.streak_model  # noqa: F401
        from src.infrastructure.database.models.catalogue_model import CatalogueModel  # noqa: F401

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSession(engine) as session:
            count = await session.scalar(select(func.count()).select_from(CatalogueModel))
            if count == 0:
                seed_data = [
                    CatalogueModel(catalogue_type="category", name="health", description="Salud"),
                    CatalogueModel(catalogue_type="category", name="productivity", description="Productividad"),
                    CatalogueModel(catalogue_type="category", name="learning", description="Aprendizaje"),
                    CatalogueModel(catalogue_type="frequency", name="daily", description="Todos los días"),
                    CatalogueModel(catalogue_type="frequency", name="weekly", description="Una vez por semana"),
                    CatalogueModel(catalogue_type="frequency", name="monthly", description="Una vez por mes"),
                    CatalogueModel(catalogue_type="habit_type", name="positive", description="Hábito para adquirir"),
                    CatalogueModel(catalogue_type="habit_type", name="negative", description="Hábito para eliminar"),
                ]
                session.add_all(seed_data)
                await session.commit()
                print("✅ Catálogos sembrados correctamente")
            else:
                print(f"ℹ️  Catálogos ya existen ({count} registros), seed omitido")
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
