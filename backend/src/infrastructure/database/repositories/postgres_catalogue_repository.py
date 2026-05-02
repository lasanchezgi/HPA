from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models.catalogue_model import CatalogueModel


class PostgresCatalogueRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_id_by_type_and_code(
        self, catalogue_type: str, code: str
    ) -> UUID | None:
        stmt = select(CatalogueModel.id).where(
            CatalogueModel.catalogue_type == catalogue_type,
            func.lower(CatalogueModel.name) == code.lower(),
            CatalogueModel.is_active.is_(True),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_code_by_id(self, catalogue_id: UUID) -> str | None:
        stmt = select(func.lower(CatalogueModel.name)).where(
            CatalogueModel.id == catalogue_id,
            CatalogueModel.is_active.is_(True),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
