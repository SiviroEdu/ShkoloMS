from datetime import datetime

from fastapi import HTTPException, status
import jwt
import pydantic

from app import TokenData
from app.settings import SECRET_KEY, ALGORITHM


async def decrypt_token(token: str) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        try:
            token_data = TokenData(**payload)
        except pydantic.ValidationError as e:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    return token_data


def create_access_token(data: dict, expires_timestamp: int):
    to_encode = data.copy()

    expire = datetime.fromtimestamp(expires_timestamp)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
