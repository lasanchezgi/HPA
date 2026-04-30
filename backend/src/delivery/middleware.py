from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.domain.exceptions import (
    ApplicationException,
    DomainException,
    DuplicateHabitError,
    DuplicateLogError,
    HabitNotFoundError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        try:
            return await call_next(request)
        except HabitNotFoundError as exc:
            return JSONResponse(status_code=404, content={"detail": str(exc)})
        except UserNotFoundError as exc:
            return JSONResponse(status_code=404, content={"detail": str(exc)})
        except InvalidCredentialsError as exc:
            return JSONResponse(status_code=401, content={"detail": str(exc)})
        except UserAlreadyExistsError as exc:
            return JSONResponse(status_code=409, content={"detail": str(exc)})
        except DuplicateHabitError as exc:
            return JSONResponse(status_code=409, content={"detail": str(exc)})
        except DuplicateLogError as exc:
            return JSONResponse(status_code=409, content={"detail": str(exc)})
        except (DomainException, ApplicationException) as exc:
            return JSONResponse(status_code=422, content={"detail": str(exc)})
