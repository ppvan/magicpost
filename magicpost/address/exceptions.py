from fastapi import HTTPException, status


class ProvinceNotFound(HTTPException):
    def __init__(self, message="Provice not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class DistrictNotFound(HTTPException):
    def __init__(self, message="District not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class WardNotFound(HTTPException):
    def __init__(self, message="Ward not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
