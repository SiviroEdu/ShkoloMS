from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app import UserSchema
from app.auth import decrypt_token, create_access_token
from app.bridges.users import UsersBridge
from app.shkolo_wrap import update_user_data

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserSchema | None:
    token_data = await decrypt_token(token)
    # async with session.get(
    #     f"https://app.shkolo.bg/ajax/diary/getAbsencesForPupil",
    #     cookies={
    #         "remember_customSession_" + token_data.shkolo_token_id: token_data.shkolo_token
    #     }
    # ) as resp:
    #     if (await resp.content.read(9)).decode() == "<!DOCTYPE":
    #         raise credentials_exception

    user = await UsersBridge.get_by_username(token_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


router.add_api_route("/get-current-user", get_current_user)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # result = await login_shkolo(form_data.username, form_data.password)

    # if not result:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Error during login, might be incorrect "
    #                "username or password or Shkolo related error.",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # cookie, pupil_id = result

    await update_user_data(form_data.username, True, True)

    access_token = create_access_token(
        data={
            # "shkolo_token_id": cookie.get("name").split("_")[-1],
            # "shkolo_token": cookie.get("value"),
            "username": form_data.username
        },
        expires_timestamp=int(
            (datetime.now() + timedelta(days=365)
        ).timestamp())
    )

    return {"access_token": access_token, "token_type": "bearer"}
