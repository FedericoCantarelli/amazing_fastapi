"""Ready response model."""

from pydantic import BaseModel, Field


class ReadyResponse(BaseModel):
    api: str = Field(..., description="API state", examples=["ready"])
    sha: str = Field(..., description="SHA of the source code", examples=["haj78ka"])
    env: str = Field(..., description="Running environment", examples=["local"])
    version: str = Field(..., description="Version of the API", examples=["0.5.0"])

    class ConfigDict:
        json_schema_extra = {
            "example": {"api": "ready", "sha": "haj78ka", "env": "test"}
        }
