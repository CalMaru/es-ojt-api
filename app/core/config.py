from pydantic import Field
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    # API Setting
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_WORKERS: int = Field(default=6, env="API_WORKERS")
    API_THREADS: int = Field(default=6, env="API_THREADS")

    # Data Files
    DATA_PATH: str = Field(default="/file/es-ojt", env="DATA_PATH")


env_config = EnvSettings()
