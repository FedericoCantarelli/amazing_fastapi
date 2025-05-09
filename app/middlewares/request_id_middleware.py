import uuid
from contextvars import ContextVar
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Context variable
correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id.set(uuid.uuid4().hex)
        response = await call_next(request)
        return response
