from fastapi import APIRouter, HTTPException, status

from app.settings import driver
from app.shkolo_wrap import save_cookie_enc, get_cookie_enc, login_shkolo, get_grades

router = APIRouter(prefix="/misc")


@router.get("/enc")
async def misc():
    return await save_cookie_enc("hi", "test", 2400253553, expiry=123124124)


@router.get("/dec")
async def misc():
    return await get_cookie_enc("hi", 2400253553)


@router.get("/login")
async def misc():
    cookie = await login_shkolo("RimnaIb", "Ibrrimma271272")

    if not cookie:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Couldn't extract remember session cookie. "
            "Might be your mistake, ours or Shkolo's."
        )

    return cookie

@router.get("/grade")
async def misc():
    return await get_grades(2400253553)
