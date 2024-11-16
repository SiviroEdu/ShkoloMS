from typing import Annotated

from fastapi import APIRouter, Depends

from app import UserSchema
from app.routers.auth import get_current_user
from app.shkolo_wrap import update_user_data

router = APIRouter(prefix="/data")

#
# @router.get("/enc", tags=["dev"])
# async def misc():
#     return await save_cookie_enc("hi", "test", 2400253553, expiry=123124124)
#
#
# @router.get("/dec", tags=["dev"])
# async def misc():
#     return await get_cookie_enc("hi", 2400253553)
#


# @router.get("/login")
# async def misc():
#     cookie = await login_shkolo("RimnaIb", "Ibrrimma271272")
#
#     if not cookie:
#         raise HTTPException(
#             status.HTTP_400_BAD_REQUEST,
#             "Couldn't extract remember session cookie. "
#             "Might be your mistake, ours or Shkolo's."
#         )
#
#     return cookie

@router.get("/update")
async def update(user: Annotated[UserSchema, Depends(get_current_user)]):
    return await update_user_data(user.shkolo_username, feedbacks=True)

# @router.get("/grade", tags=["dev"])
# async def misc():
#     return await get_grades(2400253553)
