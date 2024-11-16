from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app import LoginCookie, Pupil
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

LoginCookieSchema = pydantic_model_creator(LoginCookie, name="LoginCookieSchema")
LoginCookieCreate = pydantic_model_creator(
    LoginCookie,
    name="LoginCookieCreate",
    exclude_readonly=True,
)

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