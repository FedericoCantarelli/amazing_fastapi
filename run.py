"""Entrypoint for the application once deployed.
This script is responsible for running the FastAPI application using Uvicorn."""

import os
import uvicorn
from dotenv import load_dotenv

EXCLUDE_RELOAD_PATH: list[str] = []

reload = True if os.environ.get("ENVIRONMENT", "local") == "local" else False


if __name__ == "__main__":
    port: int = int(os.environ.get("PORT", 8080))
    if os.environ.get("ENVIRONMENT", "local") == "local":
        load_dotenv("./.env.development")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        reload_excludes=EXCLUDE_RELOAD_PATH if reload else None,
    )
