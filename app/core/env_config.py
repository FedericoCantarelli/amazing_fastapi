from pydantic_settings import BaseSettings

config = None


class EnvConfig(BaseSettings):
    """
    Config class for environment settings.
    """

    environment: str
    sha: str

    def get_env(self) -> str:
        return self.environment

    def get_sha(self) -> str:
        return self.sha


def get_env_config() -> EnvConfig:
    global config
    if not config:
        config = EnvConfig()
    return config
