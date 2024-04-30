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
    ES_PORT: int = Field(default=9200, env="ES_PORT")
    ES_USERNAME: str = Field(default="elastic", env="ES_USERNAME")
    ES_PASSWORD: str = Field(default="42maru", env="ES_PASSWORD")

    @property
    def ES_CONFIG(self) -> dict:
        return {"host": "localhost", "port": 9200}
        # return f"http://{self.ES_HOST}:{self.ES_PORT}"


env_config = EnvSettings()
