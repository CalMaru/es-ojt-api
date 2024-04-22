from app.core.config import env_config

bind = f"{env_config.API_HOST}:{env_config.API_PORT}"
workers = f"{env_config.API_WORKERS}"
wsgi_app = "app.__main__:es_app"
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
timeout = 60
