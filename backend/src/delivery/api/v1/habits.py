import asyncio
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dtos.habit_dtos import CreateHabitDTO, LogCompletionDTO, UpdateHabitDTO
from src.application.use_cases.habits.archive_habit import ArchiveHabitUseCase
from src.application.use_cases.habits.create_habit import CreateHabitUseCase
from src.application.use_cases.habits.get_habit_logs import GetHabitLogsUseCase
from src.application.use_cases.habits.get_user_habits import GetUserHabitsUseCase
from src.application.use_cases.habits.log_completion import LogCompletionUseCase
from src.application.use_cases.habits.update_habit import UpdateHabitUseCase
from src.delivery.dependencies import (
    CurrentUser,
    DbSession,
    get_archive_habit_use_case,
    get_create_habit_use_case,
    get_habit_logs_use_case,
    get_log_completion_use_case,
    get_update_habit_use_case,
    get_user_habits_use_case,
)
from src.delivery.schemas.habit_schemas import (
    CreateHabitRequest,
    HabitDetailResponse,
    HabitLogSchema,
    HabitResponse,
    LogCompletionRequest,
    LogCompletionResponse,
    UpdateHabitRequest,
)
from src.domain.exceptions import HabitNotFoundError
from src.infrastructure.database.repositories.postgres_catalogue_repository import (
    PostgresCatalogueRepository,
)
from src.infrastructure.database.repositories.postgres_streak_repository import (
    PostgresStreakRepository,
)

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit(
    body: CreateHabitRequest,
    current_user: CurrentUser,
    db: DbSession,
    use_case: Annotated[CreateHabitUseCase, Depends(get_create_habit_use_case)],
) -> HabitResponse:
    catalogue_repo = PostgresCatalogueRepository(db)

    frequency_id = await catalogue_repo.find_id_by_type_and_code("frequency", body.frequency_code)
    if not frequency_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown frequency_code: '{body.frequency_code}'",
        )

    category_id = await catalogue_repo.find_id_by_type_and_code("category", body.category_code)
    if not category_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown category_code: '{body.category_code}'",
        )

    dto = CreateHabitDTO(
        user_id=current_user.id,
        habit_name=body.habit_name,
        habit_description=body.habit_description,
        frequency_id=frequency_id,
        category_id=category_id,
        habit_type_id=body.habit_type_id,
        goal_target=body.goal_target,
        habit_start_date=body.habit_start_date,
        habit_end_date=body.habit_end_date,
    )
    habit = await use_case.execute(dto)
    return HabitResponse(
        **habit.__dict__,
        frequency_code=body.frequency_code,
        category_code=body.category_code,
    )


@router.get("/", response_model=list[HabitResponse])
async def list_habits(
    current_user: CurrentUser,
    db: DbSession,
    use_case: Annotated[GetUserHabitsUseCase, Depends(get_user_habits_use_case)],
    active_only: bool = False,
) -> list[HabitResponse]:
    habits = await use_case.execute(current_user.id, active_only=active_only)
    if not habits:
        return []
    catalogue_repo = PostgresCatalogueRepository(db)
    unique_ids = list({h.frequency_id for h in habits} | {h.category_id for h in habits})
    codes = await asyncio.gather(*[catalogue_repo.find_code_by_id(uid) for uid in unique_ids])
    code_map: dict[UUID, str] = {uid: code or "" for uid, code in zip(unique_ids, codes)}
    return [
        HabitResponse(
            **h.__dict__,
            frequency_code=code_map.get(h.frequency_id, ""),
            category_code=code_map.get(h.category_id, ""),
        )
        for h in habits
    ]


@router.get("/{habit_id}", response_model=HabitDetailResponse)
async def get_habit(
    habit_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
    use_case: Annotated[GetUserHabitsUseCase, Depends(get_user_habits_use_case)],
) -> HabitDetailResponse:
    habits = await use_case.execute(current_user.id)
    habit = next((h for h in habits if h.id == habit_id), None)
    if not habit:
        raise HTTPException(status_code=404, detail=f"Habit '{habit_id}' not found.")

    catalogue_repo = PostgresCatalogueRepository(db)
    streak_repo = PostgresStreakRepository(db)

    frequency_code = await catalogue_repo.find_code_by_id(habit.frequency_id) or ""
    category_code = await catalogue_repo.find_code_by_id(habit.category_id) or ""
    streak = await streak_repo.find_by_habit_id(habit_id)

    return HabitDetailResponse(
        **habit.__dict__,
        frequency_code=frequency_code,
        category_code=category_code,
        current_streak=streak.current_streak if streak else 0,
        best_streak=streak.best_streak if streak else 0,
    )


@router.get("/{habit_id}/logs", response_model=list[HabitLogSchema])
async def get_habit_logs(
    habit_id: UUID,
    current_user: CurrentUser,
    use_case: Annotated[GetHabitLogsUseCase, Depends(get_habit_logs_use_case)],
) -> list[HabitLogSchema]:
    try:
        logs = await use_case.execute(habit_id, current_user.id)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail=f"Habit '{habit_id}' not found.")
    return [
        HabitLogSchema(
            id=log.id,
            habit_id=log.habit_id,
            status=log.status,
            logged_at=log.logged_at,
            notes=log.notes,
        )
        for log in logs
    ]


@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: UUID,
    body: UpdateHabitRequest,
    current_user: CurrentUser,
    db: DbSession,
    use_case: Annotated[UpdateHabitUseCase, Depends(get_update_habit_use_case)],
) -> HabitResponse:
    catalogue_repo = PostgresCatalogueRepository(db)

    frequency_id = None
    if body.frequency_code is not None:
        frequency_id = await catalogue_repo.find_id_by_type_and_code("frequency", body.frequency_code)
        if not frequency_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unknown frequency_code: '{body.frequency_code}'",
            )

    category_id = None
    if body.category_code is not None:
        category_id = await catalogue_repo.find_id_by_type_and_code("category", body.category_code)
        if not category_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Unknown category_code: '{body.category_code}'",
            )

    dto = UpdateHabitDTO(
        habit_id=habit_id,
        user_id=current_user.id,
        habit_name=body.habit_name,
        habit_description=body.habit_description,
        frequency_id=frequency_id,
        category_id=category_id,
        goal_target=body.goal_target,
        habit_end_date=body.habit_end_date,
    )
    try:
        habit = await use_case.execute(dto)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail=f"Habit '{habit_id}' not found.")
    freq_code, cat_code = await asyncio.gather(
        catalogue_repo.find_code_by_id(habit.frequency_id),
        catalogue_repo.find_code_by_id(habit.category_id),
    )
    return HabitResponse(
        **habit.__dict__,
        frequency_code=freq_code or "",
        category_code=cat_code or "",
    )


@router.patch("/{habit_id}/archive", status_code=status.HTTP_204_NO_CONTENT)
async def archive_habit(
    habit_id: UUID,
    current_user: CurrentUser,
    use_case: Annotated[ArchiveHabitUseCase, Depends(get_archive_habit_use_case)],
) -> None:
    try:
        await use_case.execute(habit_id, current_user.id)
    except HabitNotFoundError:
        raise HTTPException(status_code=404, detail=f"Habit '{habit_id}' not found.")


@router.post(
    "/{habit_id}/logs",
    response_model=LogCompletionResponse,
    status_code=status.HTTP_201_CREATED,
)
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
        logged_at=result.logged_at,
    )
