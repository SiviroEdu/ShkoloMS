import re
from pathlib import Path

import aiofiles

from app.settings import source_path

PUPIL_ID_PATTERN = r'<input id="pupil_id_field"[^>]*value="(\d+)"'

async def get_pupil_id() -> int:
    async with aiofiles.open(source_path / "metadata.html", encoding="utf8", mode="r") as f:
        contents = await f.read()

    return re.search(PUPIL_ID_PATTERN, contents, re.DOTALL).group(1)

