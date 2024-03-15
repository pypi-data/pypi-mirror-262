from __future__ import annotations

from typing_extensions import Literal

import httpx


__all__ = [
    "BadRequestError",
    "AuthenticationError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "InternalServerError",
]


class PigeonsAIError(Exception):
    pass


class APIStatusError():
    """Raised when an API response has a status code of 4xx or 5xx."""

    response: httpx.Response
    status_code: int

    def __init__(self, message: str, *, response: httpx.Response, body: object | None) -> None:
        super().__init__(message, response.request, body=body)
        self.response = response
        self.status_code = response.status_code


class BadRequestError(APIStatusError):
    status_code: Literal[400] = 400  


class AuthenticationError(APIStatusError):
    status_code: Literal[401] = 401  


class NotFoundError(APIStatusError):
    status_code: Literal[404] = 404  


class ConflictError(APIStatusError):
    status_code: Literal[409] = 409  


class UnprocessableEntityError(APIStatusError):
    status_code: Literal[422] = 422  


class InternalServerError(APIStatusError):
    pass
