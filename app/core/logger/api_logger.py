from app.core.logger.base_logger import Logger


class AppLogger(Logger):
    def __init__(self):
        super().__init__("es-ojt-api")

    def error(self, traceback: str):
        self.logger.error(traceback)


app_logger = AppLogger()
