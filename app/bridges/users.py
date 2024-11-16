import os

from app import UserSchema, UserCreate
from app.settings import session


class UsersBridge:
    base_url = os.environ["USERS_MS_URL"]

    @classmethod
    async def create(cls, payload: UserCreate) -> UserSchema:
        async with session.post(cls.base_url + "/users/", json=payload.model_dump()) as resp:
            content = await resp.json()

            if resp.status == 422:
                raise ValueError(content)

            return content

    @staticmethod
    async def _fetch_user(url) -> UserSchema:
        async with session.get(url) as resp:
            print(await resp.read())
            data = await resp.json()

            return UserSchema(**data) if data else None

    @classmethod
    async def get_by_id(cls, id_: int) -> UserSchema:
        url = cls.base_url + f"/users/{id_}"

        return await cls._fetch_user(url)

    @classmethod
    async def get_by_username(cls, username: str) -> UserSchema:
        url = cls.base_url + f"/users/username/{username}"

        return await cls._fetch_user(url)

    @classmethod
    async def get_by_pupil_id(cls, id_: int) -> UserSchema:
        url = cls.base_url + f"/users/pupil_id/{id_}"

        return await cls._fetch_user(url)
