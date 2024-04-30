from app.core.logger.base_logger import Logger


class ElasticsearchLogger(Logger):
    def __init__(self):
        super().__init__("elasticsearch")

        def connect(connected: bool):
            if connected:
                self.logger.info("Connecting to Elasticsearch Client")
            else:
                self.logger.error("Failed to connect Elasticsearch Client")

        def close():
            self.logger.info("Closing Elasticsearch Client")


es_logger = ElasticsearchLogger()
