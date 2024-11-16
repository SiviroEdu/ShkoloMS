from typing import Annotated

from fastapi import Depends, APIRouter

from app import UserSchema
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/@me")
async def get_me(user: Annotated[UserSchema, Depends(get_current_user)]):
    return user
