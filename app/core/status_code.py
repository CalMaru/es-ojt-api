from enum import Enum


class StatusCode(Enum):
    C20000 = "OK"

    C50000 = "System Error"
    C50001 = "Elasticsearch Error"

    @property
    def code(self):
        return self.name

    @property
    def message(self):
        return self.value

    def response(self):
        return {
            "response_code": self.code,
            "response_message": self.value,
        }
