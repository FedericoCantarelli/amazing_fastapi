from typing import Annotated
from app.core import get_env_config, EnvConfig
from fastapi import Depends

config_dependency = Annotated[EnvConfig, Depends(get_env_config)]
