from pydantic import Field
from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    # API Setting
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_WORKERS: int = Field(default=6, env="API_WORKERS")
    API_THREADS: int = Field(default=6, env="API_THREADS")

    # Elasticsearch Config
    ES_HOST: str = Field(default="localhost", env="ES_HOST")
    ES_PORT: int = Field(default=90922, env="ES_PORT")
    ES_USERNAME: str = Field(default="42maru", env="ES_USERNAME")
    ES_PASSWORD: str = Field(default="42maru", env="ES_PASSWORD")

    # Data Files
    DATA_PATH: str = Field(default="/file/es-ojt", env="DATA_PATH")

    @property
    def ES_CONFIG(self) -> list[dict]:
        es_host = dict()
        es_host["host"] = self.ES_HOST
        es_host["port"] = self.ES_PORT
        es_host["scheme"] = "http"
        return [es_host]


env_config = EnvSettings()
