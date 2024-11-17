from datetime import datetime

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, ConfigDict

from app import Pupil
from app.models import Feedback, Grade, Course

Tortoise.init_models(
    ["app.models"], "models"
)

FeedbackSchema = pydantic_model_creator(Feedback, name="FeedbackSchema")
FeedbackCreate = pydantic_model_creator(
    Feedback,
    name="FeedbackCreate",
    exclude_readonly=True,
)

# LoginCookieSchema = pydantic_model_creator(LoginCookie, name="LoginCookieSchema")
# LoginCookieCreate = pydantic_model_creator(
#     LoginCookie,
#     name="LoginCookieCreate",
#     exclude_readonly=True,
# )

PupilSchema = pydantic_model_creator(Pupil, name="PupilSchema")
class PupilCreate(pydantic_model_creator(
    Pupil,
    name="PupilCreate",
    exclude_readonly=True,
)):
    id: int

GradeSchema = pydantic_model_creator(Grade, name="GradeSchema")
GradeCreateGenerated = pydantic_model_creator(
    Grade,
    name="GradeCreate",
    exclude_readonly=True,
)

class GradeCreate(GradeCreateGenerated):
    id: int


CourseSchema = pydantic_model_creator(Course, name="CourseSchema")
CourseCreate = pydantic_model_creator(
    Course,
    name="CourseCreate",
    exclude_readonly=True,
)


class UserSchema(BaseModel):
    id: int
    shkolo_username: str | None
    shkolo_name: str | None
    pupil_id: int
    coins: int
    bulbs: int
    type: int
    created_at: datetime


class UserCreate(BaseModel):
    shkolo_username: str = None
    shkolo_name: str = None
    pupil_id: int
    coins: int = None
    bulbs: int = None
    type: int = 0


class TokenData(BaseModel):
    model_config = ConfigDict(extra="allow")
    username: str
    type: int
    # shkolo_token_id: str
    # shkolo_token: str
    exp: int
