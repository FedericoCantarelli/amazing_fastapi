from typing import Annotated

from fastapi import Depends

from app.core import EnvConfig, get_env_config

config_dependency = Annotated[EnvConfig, Depends(get_env_config)]
