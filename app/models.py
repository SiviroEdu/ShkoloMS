from ms_core import AbstractModel
from tortoise import fields


class YearClass(AbstractModel):
    id = fields.BigIntField(pk=True, generated=False)

    pupils: fields.ReverseRelation["Pupil"]
    courses: fields.ReverseRelation["Course"]

    class Meta:
        table = "year_class"


class Course(AbstractModel):
    id = fields.BigIntField(pk=True, generated=False)
    name = fields.TextField()

    year_class: fields.ForeignKeyRelation[YearClass] = fields.ForeignKeyField(
        "models.YearClass", "courses"
    )

    class Meta:
        table = "courses"


class Pupil(AbstractModel):
    id = fields.BigIntField(pk=True, generated=False)
    # user_id = fields.IntField(unique=True)

    year_class: fields.ForeignKeyRelation[YearClass] = fields.ForeignKeyField(
        "models.YearClass", "pupils", null=True
    )
    login_cookie: fields.ReverseRelation["LoginCookie"]
    grades: fields.ReverseRelation["Grade"]
    feedbacks: fields.ReverseRelation["Feedback"]

    class Meta:
        table = "pupils"


class Feedback(AbstractModel):
    name = fields.CharField(64, null=True)

    course: fields.ForeignKeyRelation[Course] = fields.ForeignKeyField(
        "models.Course", "feedbacks"
    )
    pupil: fields.ForeignKeyRelation[Pupil] = fields.ForeignKeyField(
        "models.Pupil", "feedbacks"
    )

    class Meta:
        table = "feedbacks"


class Grade(AbstractModel):
    id = fields.BigIntField(pk=True, generated=False)
    value = fields.CharField(1)

    course: fields.ForeignKeyRelation[Course] = fields.ForeignKeyField(
        "models.Course", "grades"
    )
    pupil: fields.ForeignKeyRelation[Pupil] = fields.ForeignKeyField(
        "models.Pupil", "grades"
    )

    class Meta:
        table = "grades"


class LoginCookie(AbstractModel):
    name = fields.CharField(256)
    value = fields.TextField()
    expiry = fields.BigIntField(null=True)

    pupil: fields.OneToOneRelation[Pupil] = fields.OneToOneField(
        "models.Pupil", "login_cookie"
    )

    class Meta:
        table = "login_cookies"
