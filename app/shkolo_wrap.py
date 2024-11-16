import re
from time import sleep

import aiohttp
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from app import LoginCookieCRUD, GradeCRUD, GradeCreate, CourseCRUD, LoginCookieCreate, PupilCRUD, PupilCreate
from app.settings import fernet, driver

REMEMBER_COOKIE_STARTS = "remember_customSession_"
# GRADE_BTN_REGEX = r"<button[^>]*class=\"[^\"]*grade[^>]*>(\d+)<\/button>"
PUPIL_ID_PATTERN = r'<input id="pupil_id_field"[^>]*value="(\d+)"'
CLASS_ID_PATTERN = r'<input id="class_year_id_field"[^>]*value="(\d+)"'
TABLE_PATTERN = r'<table[^>]*id="tableGrades"[^>]*>(.*?)</table>'
COURSE_GRADES_REGEX = (
    r'data-course-id="(\d+)"[\s\S]*?<td>\s*<i[^>]*></i>\s*([^<]+)</td>'   # Capture course_id and course_name
    r'|id="grade_(\d+)"[^>]*>(\d+)'                                       # Capture grade_id and grade_value
)

def simulate_login(driver, username: str, password: str):
    driver.get("https://app.shkolo.bg/auth/login")

    username_input = driver.find_element(By.ID, "login-username")
    password_input = driver.find_element(By.ID, "passwordField")
    remember = driver.find_element(By.NAME, "remember")
    login_btn = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div[1]/form/div[3]/button"))
    )

    username_input.send_keys(username)
    password_input.send_keys(password)
    remember.click()

    login_btn.click()


async def login_shkolo(username, password) -> dict | None:
    simulate_login(driver, username, password)
    sleep(1)

    pupil_id = re.search(r'data-pupil_id="(\d+)"', driver.page_source).group(1)

    if not (await PupilCRUD.get_by(id=pupil_id)):
        await PupilCRUD.create(PupilCreate(id=pupil_id))

    login_cookie = None
    for cookie in driver.get_cookies():
        if cookie["name"].startswith(REMEMBER_COOKIE_STARTS):
            login_cookie = cookie
            await save_cookie_enc(
                cookie["name"],
                cookie["value"],
                pupil_id,
                cookie.get("expiry", None),
            )
            break

    return login_cookie


async def save_cookie_enc(name, value: str, pupil_id, expiry: int = None):
    if await LoginCookieCRUD.get_by(pupil_id=pupil_id, name=name):
        await LoginCookieCRUD.update_by(
            dict(expiry=expiry),
            name=name,
            pupil_id=pupil_id
        )
    else:
        await LoginCookieCRUD.create(LoginCookieCreate(
            name=name, expiry=expiry, value=value, pupil_id=pupil_id
        ))


async def get_cookie_enc(name: str, pupil_id: int):
    record = await LoginCookieCRUD.get_by(pupil__id=pupil_id, name=name)

    return fernet.decrypt(record.value)


async def get_grades(pupil_id):
    auth_cookie = (await LoginCookieCRUD.filter_by(pupil__id=pupil_id))[0]

    value = fernet.decrypt(auth_cookie.value).decode()
    session = aiohttp.ClientSession(cookies={auth_cookie.name: value})

    async with session.get(f"https://app.shkolo.bg/ajax/diary/getGradesForPupil?pupil_id={pupil_id}") as resp:
        content = (await resp.read()).decode()

    table_match = re.search(TABLE_PATTERN, content, re.DOTALL)

    if not table_match:
        raise ValueError("Grades table not found")

    table = table_match.group(1)

    course_id = None
    for match in re.findall(COURSE_GRADES_REGEX, table):
        if match[0]:  # Captured a course_id
            course_id = match[0]
            course_name = match[1].strip()

            await CourseCRUD.get_or_create(id=course_id, name=course_name)
        else:  # Captured a grade id and value
            await GradeCRUD.create(GradeCreate(
                id=match[2], value=match[3], course_id=course_id, pupil_id=pupil_id
            ))

    await session.close()