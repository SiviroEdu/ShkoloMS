import os

from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

db_url = os.environ["DB_URL"]
fernet = Fernet(os.environ["FERNET_KEY"])

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
