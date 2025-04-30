from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.utils import get_openapi
from app.core.exceptions import HTTPException, http_exception_handler
from app.routers.healthcheck import router as ready_router
from app.__version__ import version


import logging

from app.core import setup_logging

setup_logging()
logger = logging.getLogger("app")

tags_metadata = [
    {
        "name": "Health Check",
        "description": "Get the health status of the API.",
    }
]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Proposal API",
        description="""API for evaluating commercial proposals in TechnoGym.""",
        routes=app.routes,
        version="1.0",
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Technogym_Logo.svg/640px-Technogym_Logo.svg.png"
    }
    openapi_schema["tags"] = tags_metadata
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the app, any additional setup can be done here")
    yield
    logger.info("Shutting down the app, any additional cleanup can be done here")


app = FastAPI(
    title="A simple API interface",
    version=version,
    description="<h2>Custom HTML</h2><p>Here you can set some custom html</p>",
    # docs_url=None,  # disable docs
    # redoc_url=None,  # disable redoc
    lifespan=lifespan,
    openapi_tags=tags_metadata,
)


# disable docs path
# @app.get("/docs", include_in_schema=False)
# async def override_doc():
#     """Docs access by URL is disabled in test and production environments. In local environment, the docs are available at /docs."""
#     if os.getenv("ENV") != "local":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             content=ErrorResponse(
#                 code=status.HTTP_403_FORBIDDEN,
#                 message="Doc is not publicly available",
#             ).model_dump(exclude_none=True),
#         )
#     return get_redoc_html(
#         openapi_url="/openapi.json",
#         title="Proposal API - Docs",
#     )


# # Disable redoc path
# @app.get("/redoc", include_in_schema=False)
# async def override_redoc():
#     """Redoc documentation is unavailable in test and production environments."""
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         content=ErrorResponse(
#             code=status.HTTP_403_FORBIDDEN,
#             message="Path disabled",
#         ).model_dump(exclude_none=True),
#     )


app.include_router(ready_router)
logger.info("Healthchek router added")

app.add_exception_handler(HTTPException, http_exception_handler)
logger.info("HTTPException handler added")

# Add middleware in test and local environments
# if os.getenv("ENV") in ["local", "test"]:
#     from app.middleware.debug_middleware import DebugMiddleware

#     app.add_middleware(DebugMiddleware)
#     logger.debug("AuthMiddleware added")
