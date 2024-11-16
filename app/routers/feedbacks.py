# from typing import Annotated
#
from fastapi import Depends, APIRouter
#
# from app import UserSchema, Feedback
# from app.routers.auth import get_current_user
#
router = APIRouter(
    prefix="/feedbacks",
    tags=["feedbacks"],
)
#
# @router.get("/@me")
# async def get_feedbacks(user: Annotated[UserSchema, Depends(get_current_user)]):
#     feedbacks =  await Feedback.filter(pupil_id=user.pupil_id)
#
#     return feedbacks
