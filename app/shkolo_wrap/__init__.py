import aiofiles

from app.bridges.users import UsersBridge
from app.settings import source_path
from app.shkolo_wrap.feedbacks import process_feedbacks
from app.shkolo_wrap.grades import process_grades
from app.shkolo_wrap.pupil import get_pupil_id
from app.shkolo_wrap.user import process_class_user_name


async def update_grades(pupil_id: int):
    async with aiofiles.open(source_path / "grades.html", encoding="utf8", mode="r") as f:
        grades_source = await f.read()

    await process_grades(grades_source, pupil_id)


async def update_feedbacks(pupil_id: int):
    async with aiofiles.open(source_path / "feedbacks.html", encoding="utf8", mode="r") as f:
        feedbacks_source = await f.read()

    await process_feedbacks(feedbacks_source, pupil_id)


async def update_user_data(
        username: str,
        grades: bool = False,
        feedbacks: bool = False
):
    pupil_id = await get_pupil_id()

    if not (user_db := await UsersBridge.get_by_username(username)):
        user_db = await process_class_user_name(pupil_id, username)

    if grades:
        await update_grades(pupil_id)

    if feedbacks:
        await update_feedbacks(pupil_id)

    return user_db
