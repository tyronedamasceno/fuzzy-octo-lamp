from fastapi import HTTPException, status

CREDENTIALS_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


INACTIVE_USER_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User is not active"
)
