from datetime import datetime, timedelta

import jwt
from jwt import PyJWTError
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from task_manager.exceptions import CREDENTIALS_ERROR, INACTIVE_USER_ERROR
from task_manager.models import (
    fake_users_db, UserInDB, User, Token, TokenData
)

router = APIRouter()

SECRET_KEY = "77118c0fe3a860704949ae331a0b62aaf6d7a4edb5618868262f3262bd19a229"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(username: str) -> UserInDB:
    if username not in fake_users_db:
        raise CREDENTIALS_ERROR

    user_dict = fake_users_db[username]
    return UserInDB(**user_dict)


def authenticate_user(username: str, password: str) -> UserInDB:
    user = get_user(username)

    if not verify_password(password, user.hashed_password):
        raise CREDENTIALS_ERROR

    return user


def create_access_token(*, data: dict,
                        expires_delta: timedelta = timedelta(minutes=15)):
    expire = datetime.utcnow() + expires_delta

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise CREDENTIALS_ERROR
        token_data = TokenData(username=username)
    except PyJWTError:
        raise CREDENTIALS_ERROR

    user = get_user(username=token_data.username)
    return user


async def get_current_active_user(current_user: User =
                                  Depends(get_current_user)):
    if not current_user.is_active:
        raise INACTIVE_USER_ERROR

    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm =
                                 Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise CREDENTIALS_ERROR
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
