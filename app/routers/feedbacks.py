from fastapi import Depends
from ms_core import BaseCRUDRouter

from app import FeedbackCRUD, FeedbackCreate, FeedbackSchema
from app.routers.auth import get_current_user

router = BaseCRUDRouter[FeedbackSchema, FeedbackCreate](
    crud=FeedbackCRUD,
    schema=FeedbackSchema,
    schema_create=FeedbackCreate,
    prefix="/feedbacks",
    tags=["feedbacks"],
    dependencies=[Depends(get_current_user)]
)
