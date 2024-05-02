import uvicorn

from app.core.config import env_config


def main():
    uvicorn.run(
        "app.__main__:es_app",
        host=env_config.API_HOST,
        port=env_config.API_PORT,
        workers=env_config.API_WORKERS,
    )


if __name__ == "__main__":
    main()
