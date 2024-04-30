from logging import Formatter, StreamHandler, getLogger
from logging.handlers import WatchedFileHandler
from os.path import join

from app.core.config import env_config

FORMAT: str = "%(asctime)-11s|%(process)-6d|%(threadName)-25s|%(name)-12s|%(levelname)-8s|%(message)s"


class Logger:
    def __init__(self, logger_name: str):
        self.logger_name = logger_name

        self.log_level = env_config.LOG_LEVEL
        self.log_path = env_config.LOG_PATH
        self.is_saving = env_config.IS_LOG_SAVING

        self.logger = None
        self.set_logger()

    def set_logger(self):
        self.logger = getLogger(self.logger_name)
        self.add_log_handlers()
        self.logger.setLevel(self.log_level)

    def add_log_handlers(self):
        self.add_handler(StreamHandler())

        if self.is_saving:
            self.add_handler(WatchedFileHandler(filename=join(self.log_path, "processor.log"), mode="a", encoding="utf-8", delay=False))

    def add_handler(self, handler: StreamHandler):
        handler.setLevel(self.log_level)
        handler.setFormatter(Formatter(FORMAT))
        self.logger.addHandler(handler)
