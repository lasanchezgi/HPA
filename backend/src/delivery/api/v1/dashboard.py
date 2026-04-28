from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.use_cases.dashboard.get_dashboard_summary import (
    GetDashboardSummaryUseCase,
)
from src.delivery.dependencies import CurrentUser, get_dashboard_use_case
from src.application.dtos.dashboard_dtos import DashboardSummaryDTO

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryDTO)
async def get_dashboard_summary(
    current_user: CurrentUser,
    use_case: Annotated[GetDashboardSummaryUseCase, Depends(get_dashboard_use_case)],
) -> DashboardSummaryDTO:
    return await use_case.execute(current_user.id)
