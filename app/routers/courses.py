from re import purge
from typing import Annotated

from fastapi import Depends, APIRouter, Query

from app import UserSchema, PupilCRUD, Pupil
from app.routers.auth import get_current_user

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)

@router.get("/@me")
async def get_courses(
        user: Annotated[UserSchema, Depends(get_current_user)],
        prefetch: bool = Query(True)
):
    if prefetch:
        pupil = await PupilCRUD.get_by(id=user.pupil_id)
        return pupil.year_class.courses

    pupil = await Pupil.get_or_none(id=user.pupil_id).prefetch_related("year_class__courses")
    return await pupil.year_class.courses
