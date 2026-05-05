"""Integration tests for PostgresCatalogueRepository."""
from uuid import uuid4

from sqlalchemy import func, select

from src.infrastructure.database.models.catalogue_model import CatalogueModel
from src.infrastructure.database.repositories.postgres_catalogue_repository import (
    PostgresCatalogueRepository,
)


async def _seed_catalogue(
    session, catalogue_type: str, name: str, *, is_active: bool = True
) -> CatalogueModel:
    # Return pre-existing row to avoid duplicate-key failures when the app
    # startup seed already populated the shared test DB.
    stmt = select(CatalogueModel).where(
        CatalogueModel.catalogue_type == catalogue_type,
        func.lower(CatalogueModel.name) == name.lower(),
        CatalogueModel.is_active == is_active,
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    entry = CatalogueModel(
        id=uuid4(),
        catalogue_type=catalogue_type,
        name=name,
        is_active=is_active,
    )
    session.add(entry)
    await session.flush()
    return entry


# --- find_id_by_type_and_code ---


async def test_find_id_by_type_and_code_returns_uuid(test_session):
    entry = await _seed_catalogue(test_session, "frequency", "daily")
    repo = PostgresCatalogueRepository(test_session)

    result = await repo.find_id_by_type_and_code("frequency", "daily")
    assert result == entry.id


async def test_find_id_by_type_and_code_case_insensitive(test_session):
    entry = await _seed_catalogue(test_session, "frequency", "Weekly")
    repo = PostgresCatalogueRepository(test_session)

    assert await repo.find_id_by_type_and_code("frequency", "weekly") == entry.id
    assert await repo.find_id_by_type_and_code("frequency", "WEEKLY") == entry.id


async def test_find_id_by_nonexistent_code_returns_none(test_session):
    repo = PostgresCatalogueRepository(test_session)
    result = await repo.find_id_by_type_and_code("frequency", "nonexistent_code_xyz")
    assert result is None


async def test_find_id_ignores_wrong_type(test_session):
    # "health" exists under "category", must not be found under "frequency"
    await _seed_catalogue(test_session, "category", "health")
    repo = PostgresCatalogueRepository(test_session)

    result = await repo.find_id_by_type_and_code("frequency", "health")
    assert result is None


async def test_find_id_ignores_inactive_entry(test_session):
    await _seed_catalogue(test_session, "frequency", "monthly", is_active=False)
    repo = PostgresCatalogueRepository(test_session)

    result = await repo.find_id_by_type_and_code("frequency", "monthly")
    assert result is None


# --- find_code_by_id ---


async def test_find_code_by_id_returns_name(test_session):
    entry = await _seed_catalogue(test_session, "category", "Health")
    repo = PostgresCatalogueRepository(test_session)

    result = await repo.find_code_by_id(entry.id)
    assert result == "Health"


async def test_find_code_by_id_unknown_uuid_returns_none(test_session):
    repo = PostgresCatalogueRepository(test_session)
    result = await repo.find_code_by_id(uuid4())
    assert result is None


async def test_find_code_by_id_ignores_inactive_entry(test_session):
    entry = await _seed_catalogue(test_session, "category", "Archived", is_active=False)
    repo = PostgresCatalogueRepository(test_session)

    result = await repo.find_code_by_id(entry.id)
    assert result is None
