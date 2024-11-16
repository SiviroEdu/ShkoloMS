from ms_core import BaseCRUD
from tortoise.contrib.pydantic import PydanticModel

from app import LoginCookie, Pupil
from app.models import Feedback, Grade, Course
from app.schemas import FeedbackSchema, LoginCookieSchema, GradeSchema, CourseSchema, LoginCookieCreate, PupilSchema
from app.settings import fernet


class FeedbackCRUD(BaseCRUD[Feedback, FeedbackSchema]):
    model = Feedback
    schema = FeedbackSchema


class LoginCookieCRUD(BaseCRUD[LoginCookie, LoginCookieSchema]):
    model = LoginCookie
    schema = LoginCookieSchema

    @classmethod
    async def create(
            cls,
            payload: LoginCookieCreate,
            **kwargs
    ) -> LoginCookieSchema:
        payload.value = fernet.encrypt(payload.value.encode()).decode()

        return await super().create(payload, **kwargs)


class PupilCRUD(BaseCRUD[Pupil, PupilSchema]):
    model = Pupil
    schema = PupilSchema


class GradeCRUD(BaseCRUD[Grade, GradeSchema]):
    model = Grade
    schema = GradeSchema


class CourseCRUD(BaseCRUD[Course, CourseSchema]):
    model = Course
    schema = CourseSchema
