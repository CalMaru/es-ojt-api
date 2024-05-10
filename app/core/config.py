from pydantic import Field
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    # API Setting
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_WORKERS: int = Field(default=6, env="API_WORKERS")
    API_THREADS: int = Field(default=6, env="API_THREADS")

    # LOG Setting
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_PATH: str = Field(default="/es-ojt-api/log", env="LOG_PATH")
    IS_LOG_SAVING: bool = Field(default=False, env="IS_LOG_SAVING")

    # Elasticsearch Config
    ES_HOST: str = Field(default="localhost", env="ES_HOST")
    ES_PORT: int = Field(default=9200, env="ES_PORT")
    ES_PIT_TIME: str = Field(default="1m", env="ES_PIT_TIME")

    @property
    def ES_CONFIG(self) -> dict:
        return {
            "hosts": f"http://{self.ES_HOST}:{self.ES_PORT}",
            "scheme": "http",
        }


env_config = EnvSettings()
