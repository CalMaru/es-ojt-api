from enum import Enum


class StatusCode(Enum):
    C20000 = "OK"

    # C421XXX - Bad Request
    C21001 = "Bad Request - start_date precedes system's start date"
    C21002 = "Bad Request - end_date has passed the system's end date"
    C21003 = "Bad Request - invalid category_type"
    C21004 = "Bad Request - invalid provider_type"
    C21005 = "Bad Request - invalid sorting"
    C21006 = "Bad Request - invalid highlight_tag.tag"

    C50000 = "System Error"
    C50001 = "Elasticsearch Error"
    C50002 = "Elasticsearch - Not Found"

    @property
    def code(self):
        return self.name

    @property
    def message(self):
        return self.value

    def response(self, extra: str = None):
        message = f"{self.message}, {extra}" if extra is not None else self.message

        return {
            "response_code": self.code,
            "response_message": message,
        }
