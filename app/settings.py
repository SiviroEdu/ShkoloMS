import os

import aiohttp
from passlib.context import CryptContext
from seleniumbase import Driver

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

db_url = os.environ["DB_URL"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# create a Driver instance with undetected_chromedriver (uc) and headless mode
driver = Driver(headless=True)

session = aiohttp.ClientSession()
