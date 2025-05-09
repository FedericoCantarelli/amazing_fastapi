"""
Healthcheck for api interface
"""

import logging

from fastapi import APIRouter
from starlette import status

from app.__version__ import version
from app.core.exceptions import HTTPException
from app.dependencies import config_dependency
from app.views import ErrorResponse, ReadyResponse

logger = logging.getLogger("app.ready")

router = APIRouter()


@router.get(
    "/error_example",
    tags=["Health Check"],
    responses={
        501: {
            "description": "Not implemented",
            "model": ErrorResponse,
        }
    },
    summary="Example of error handling",
)
async def error_example() -> None:
    logger.debug("Started GET /error_example")
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        headers={"X-Error": "There was an error"},
        content=ErrorResponse(
            code=status.HTTP_501_NOT_IMPLEMENTED,
            message="Example of error handling",
            details=[{"any": "other"}, {"details": "here"}],
        ).model_dump(exclude_none=True),
    )


@router.get(
    "/",
    tags=["Health Check"],
    responses={
        200: {
            "description": "API is ready to serve requests",
            "model": ReadyResponse,
        }
    },
    summary="Health Check for API Interface",
    status_code=200,
)
async def health_check(config: config_dependency) -> ReadyResponse:
    logger.debug("Started GET /")
    logger.info(
        "Yo. I'm ready",
        extra={
            "extra_labels": {
                "env": config.get_env(),
                "commit": config.get_sha(),
            }
        },
    )
    # Return the health check response
    logger.debug("End GET /")
    return ReadyResponse(
        api="ready", sha=config.get_sha(), env=config.get_env(), version=version
    )
