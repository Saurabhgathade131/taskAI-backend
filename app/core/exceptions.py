from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=404, detail=detail)


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=409, detail=detail)


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)