from ms_core import BaseCRUDRouter

from app import FeedbackCRUD, FeedbackCreate, FeedbackSchema

router = BaseCRUDRouter[FeedbackSchema, FeedbackCreate](
    crud=FeedbackCRUD,
    schema=FeedbackSchema,
    schema_create=FeedbackCreate,
    prefix="/feedbacks",
    tags=["feedbacks"]
)
