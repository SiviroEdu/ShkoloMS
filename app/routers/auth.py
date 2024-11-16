import time
from datetime import datetime
from typing import Annotated

import jwt
import pydantic
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import UserSchema, UserCreate, TokenData
from app.bridges.users import UsersBridge
from app.settings import session, SECRET_KEY, ALGORITHM
from app.shkolo_wrap import login_shkolo

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserSchema | None:
    time1 = time.time()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        try:
            token_data = TokenData(**payload)
        except pydantic.ValidationError as e:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    async with session.get(
        f"https://app.shkolo.bg/ajax/diary/getAbsencesForPupil",
        cookies={
            "remember_customSession_" + token_data.shkolo_token_id: token_data.shkolo_token
        }
    ) as resp:
        if (await resp.content.read(9)).decode() == "<!DOCTYPE":
            raise credentials_exception

    user = await UsersBridge.get_by_username(token_data.username)
    print(time.time() - time1)
    return user

def create_access_token(data: dict, expires_timestamp: int):
    to_encode = data.copy()

    expire = datetime.fromtimestamp(expires_timestamp)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = await login_shkolo(form_data.username, form_data.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error during login, might be incorrect "
                   "username or password or Shkolo related error.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cookie, pupil_id = result

    if not await UsersBridge.get_by_username(form_data.username):
        await UsersBridge.create(UserCreate(
            shkolo_username=form_data.username, pupil_id=pupil_id
        ))

    access_token = create_access_token(
        data={
            "shkolo_token_id": cookie.get("name").split("_")[-1],
            "shkolo_token": cookie.get("value"),
            "username": form_data.username
        },
        expires_timestamp=cookie.get("expiry")
    )

    return {"access_token": access_token, "token_type": "bearer"}
