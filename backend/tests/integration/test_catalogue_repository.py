"""Integration tests for PostgresCatalogueRepository."""
from uuid import uuid4

import pytest

from src.infrastructure.database.models.catalogue_model import CatalogueModel
from src.infrastructure.database.repositories.postgres_catalogue_repository import (
    PostgresCatalogueRepository,
)


async def _seed_catalogue(session, catalogue_type: str, name: str) -> CatalogueModel:
    entry = CatalogueModel(
        id=uuid4(),
        catalogue_type=catalogue_type,
        name=name,
        is_active=True,
    )
    session.add(entry)
    await session.flush()
    return entry


@pytest.mark.asyncio
async def test_find_id_by_type_and_code_returns_uuid(test_session):
    entry = await _seed_catalogue(test_session, "frequency", "daily")
    repo = PostgresCatalogueRepository(test_session)

    result = await repo.find_id_by_type_and_code("frequency", "daily")
    assert result == entry.id


@pytest.mark.asyncio
async def test_find_id_by_type_and_code_case_insensitive(test_session):
    entry = await _seed_catalogue(test_session, "frequency", "Weekly")
    repo = PostgresCatalogueRepository(test_session)

    result_lower = await repo.find_id_by_type_and_code("frequency", "weekly")
    result_upper = await repo.find_id_by_type_and_code("frequency", "WEEKLY")
    assert result_lower == entry.id
    assert result_upper == entry.id


@pytest.mark.asyncio
async def test_find_id_by_nonexistent_code_returns_none(test_session):
    repo = PostgresCatalogueRepository(test_session)
    result = await repo.find_id_by_type_and_code("frequency", "nonexistent_code_xyz")
    assert result is None
