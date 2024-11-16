from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

REMEMBER_COOKIE_STARTS = "remember_customSession_"


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


# async def login_shkolo(username, password) -> tuple[dict, int] | None:
#     # simulate_login(driver, username, password)
#     # sleep(1)
#
#     login_cookie = None
#     for cookie in driver.get_cookies():
#         if cookie["name"].startswith(REMEMBER_COOKIE_STARTS):
#             login_cookie = cookie
#             # await save_cookie_enc(
#             #     cookie["name"],
#             #     cookie["value"],
#             #     pupil_id,
#             #     cookie.get("expiry", None),
#             # )
#             break
#
#     return login_cookie, pupil_id if login_cookie else None
