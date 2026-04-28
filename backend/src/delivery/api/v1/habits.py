from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.application.dtos.habit_dtos import CreateHabitDTO, LogCompletionDTO
from src.application.use_cases.habits.create_habit import CreateHabitUseCase
from src.application.use_cases.habits.get_user_habits import GetUserHabitsUseCase
from src.application.use_cases.habits.log_completion import LogCompletionUseCase
from src.delivery.dependencies import (
    CurrentUser,
    get_create_habit_use_case,
    get_log_completion_use_case,
    get_user_habits_use_case,
)
from src.delivery.schemas.habit_schemas import (
    CreateHabitRequest,
    HabitResponse,
    LogCompletionRequest,
    LogCompletionResponse,
)

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit(
    body: CreateHabitRequest,
    current_user: CurrentUser,
    use_case: Annotated[CreateHabitUseCase, Depends(get_create_habit_use_case)],
) -> HabitResponse:
    dto = CreateHabitDTO(
        user_id=current_user.id,
        habit_name=body.habit_name,
        habit_description=body.habit_description,
        frequency_id=body.frequency_id,
        category_id=body.category_id,
        habit_type_id=body.habit_type_id,
        goal_target=body.goal_target,
        habit_start_date=body.habit_start_date,
        habit_end_date=body.habit_end_date,
    )
    habit = await use_case.execute(dto)
    return HabitResponse(**habit.__dict__)


@router.get("/", response_model=list[HabitResponse])
async def list_habits(
    current_user: CurrentUser,
    use_case: Annotated[GetUserHabitsUseCase, Depends(get_user_habits_use_case)],
    active_only: bool = False,
) -> list[HabitResponse]:
    habits = await use_case.execute(current_user.id, active_only=active_only)
    return [HabitResponse(**h.__dict__) for h in habits]


@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(
    habit_id: UUID,
    current_user: CurrentUser,
    use_case: Annotated[GetUserHabitsUseCase, Depends(get_user_habits_use_case)],
) -> HabitResponse:
    from src.domain.exceptions import HabitNotFoundError
    from fastapi import HTTPException

    habits = await use_case.execute(current_user.id)
    habit = next((h for h in habits if h.id == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit '{habit_id}' not found.")
    return HabitResponse(**habit.__dict__)


@router.post("/{habit_id}/log", response_model=LogCompletionResponse, status_code=status.HTTP_201_CREATED)
async def log_habit_completion(
    habit_id: UUID,
    body: LogCompletionRequest,
    current_user: CurrentUser,
    use_case: Annotated[LogCompletionUseCase, Depends(get_log_completion_use_case)],
) -> LogCompletionResponse:
    dto = LogCompletionDTO(
        habit_id=habit_id,
        user_id=current_user.id,
        status=body.status,
        notes=body.notes,
        completion_value=body.completion_value,
    )
    result = await use_case.execute(dto)
    return LogCompletionResponse(
        log_id=result.log_id,
        habit_id=result.habit_id,
        status=result.status,
        current_streak=result.current_streak,
        best_streak=result.best_streak,
    )
