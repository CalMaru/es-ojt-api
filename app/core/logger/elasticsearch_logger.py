from app.core.logger.base_logger import Logger


class ElasticsearchLogger(Logger):
    def __init__(self):
        super().__init__("elasticsearch")

    def connect(self, connected: bool = None):
        if connected is None:
            self.logger.info("Connecting to Elasticsearch Client")
            return

        if connected:
            self.logger.info(f"Connecting to Elasticsearch Client: {connected}")
        else:
            self.logger.error("Failed to connect Elasticsearch Client")

    def close(self):
        self.logger.info("Closing Elasticsearch Client")


es_logger = ElasticsearchLogger()
