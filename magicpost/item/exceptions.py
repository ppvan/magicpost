from fastapi import HTTPException, status


class ItemNotFound(HTTPException):
    def __init__(self, message="Item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class NoNextZipcodeFound(HTTPException):
    def __init__(self, message="No next zipcode found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
