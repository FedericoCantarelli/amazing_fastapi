from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils import LogSetupper

logger = LogSetupper("debug_middleware").setup()


class DebugMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        logger.info(
            f"Request {request.method} received ad {request.url.path}",
            extra={
                "extra_labels": {
                    "url": request.url.path,
                    "base_url": request.base_url.path,
                    "headers": dict(request.headers),
                    "query_params": dict(request.query_params),
                    "path_params": request.path_params,
                    "client": {
                        "host": request.client.host,
                        "port": request.client.port,
                    },
                    "body": str(await request.body()),
                    "method": request.method,
                    "httpRequest": {"requestMethod": request.method},
                }
            },
        )
        return await call_next(request)
