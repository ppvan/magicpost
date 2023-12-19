from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )


class InvalidRoleUserCreation(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't create user with this role",
        )


class AuthorizationException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource",
        )


class InvalidUsernameOrPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )


class UsernameAlreadyExists(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username: {username} already exists",
        )
