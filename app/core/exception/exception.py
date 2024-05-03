from app.core.status_code import StatusCode


class BaseError(Exception):
    def __init__(self, error_code: StatusCode, status_code: int = 400):
        self.response = error_code.response()
        self.status_code = status_code


class BadRequestError(BaseError):
    def __init__(self, error_code: StatusCode, status_code: int = 400):
        super().__init__(error_code, status_code)
