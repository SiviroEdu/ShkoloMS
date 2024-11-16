from typing import Annotated

from fastapi import Depends, APIRouter

from app import UserSchema, PupilCRUD
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)

@router.get("/@me")
async def get_courses(user: Annotated[UserSchema, Depends(get_current_user)]):
    pupil = await PupilCRUD.get_by(id=user.pupil_id)

    return pupil.year_class.courses
