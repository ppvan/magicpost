from fastapi import HTTPException, status


class OfficeNotFound(HTTPException):
    def __init__(self, message="Office not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
