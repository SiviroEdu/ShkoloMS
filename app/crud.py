from ms_core import BaseCRUD

from app import LoginCookie, Pupil
from app.models import Feedback, Grade, Course
from app.schemas import FeedbackSchema, LoginCookieSchema, GradeSchema, CourseSchema, LoginCookieCreate, PupilSchema
from app.settings import pwd_context


class FeedbackCRUD(BaseCRUD[Feedback, FeedbackSchema]):
    model = Feedback
    schema = FeedbackSchema

#
# class LoginCookieCRUD(BaseCRUD[LoginCookie, LoginCookieSchema]):
#     model = LoginCookie
#     schema = LoginCookieSchema
#
#     @classmethod
#     async def create(
#             cls,
#             payload: LoginCookieCreate,
#             **kwargs
#     ) -> LoginCookieSchema:
#         payload.value = pwd_context.hash(payload.value.encode()).decode()
#
#         return await super().create(payload, **kwargs)
#
#     @classmethod
#     async def update_by(
#             cls, payload: LoginCookieCreate | dict, **kwargs
#     ) -> LoginCookieSchema | None:
#         if not (token := payload.get("value", None)):
#             raise ValueError("dict(value=token) is required")
#
#         payload["value"] = fernet.encrypt(token.encode()).decode()
#
#         return await super().update_by(payload, **kwargs)


class PupilCRUD(BaseCRUD[Pupil, PupilSchema]):
    model = Pupil
    schema = PupilSchema


class GradeCRUD(BaseCRUD[Grade, GradeSchema]):
    model = Grade
    schema = GradeSchema


class CourseCRUD(BaseCRUD[Course, CourseSchema]):
    model = Course
    schema = CourseSchema
