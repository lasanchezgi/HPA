from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse
from openai import APIError, AuthenticationError, RateLimitError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

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
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
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
        except RateLimitError:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Coach no disponible temporalmente. Intenta en unos segundos."
                },
            )
        except AuthenticationError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Coach no configurado correctamente."},
            )
        except APIError:
            return JSONResponse(
                status_code=502,
                content={
                    "detail": "Error comunicándose con el coach. Intenta de nuevo."
                },
            )
