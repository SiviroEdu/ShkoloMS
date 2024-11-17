import re
from pathlib import Path

import aiofiles

from app import PupilCRUD, YearClass, UserCreate, UserSchema
from app.bridges.users import UsersBridge
from .pupil import get_pupil_id
from ..settings import source_path

USER_NAME_CLASS_PATTERN = r'<i class="fas fa-user-graduate"></i>\s*([\w\s.]+),\s*(\d+\w)'
CLASS_ID_PATTERN = r'<input id="class_year_id_field"[^>]*value="(\d+)"'


async def get_class_id() -> int:
    async with aiofiles.open(source_path / "metadata.html", encoding="utf8", mode="r") as f:
        contents = await f.read()

    return re.search(CLASS_ID_PATTERN, contents, re.DOTALL).group(1)


async def process_class_user_name(
    pupil_id: int, username: str
) -> UserSchema:
    async with aiofiles.open(source_path / "metadata.html", encoding="utf8", mode="r") as f:
        source = await f.read()

    class_id = await get_class_id()

    user_name_class = re.search(USER_NAME_CLASS_PATTERN, source, re.DOTALL)
    user_name = user_name_class.group(1)
    class_name = user_name_class.group(2)

    _, class_existed = await YearClass.get_or_create(
        dict(name=class_name), id=class_id
    )
    _, pupil_existed = await PupilCRUD.get_or_create(
        year_class_id=class_id, id=pupil_id
    )
    user = await UsersBridge.create(UserCreate(
        pupil_id=pupil_id, shkolo_name=user_name, shkolo_username=username
    ))

    return user
