from operator import contains
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

@pytest.fixture()
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(r"C:\Users\Виталий\.wdm\drivers\chromedriver\win64\131.0.6778.264\chromedriver-win32\chromedriver.exe")
    config_driver = webdriver.Chrome(service=service, options=options)
    yield config_driver
    config_driver.quit()



def test_task4(driver):
    options = Options()
    service = Service(r"C:\Users\Виталий\.wdm\drivers\chromedriver\win64\131.0.6778.264\chromedriver-win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.google.com/?hl=ru")
    lucky_button = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Мне повезёт!']")
    assert lucky_button is not None
    # driver_ru.get("https://www.google.com")
    # assert driver_ru.execute_script("return navigator.language") == "ru-RU", \
    #     "Текущий язык браузера не русский"






