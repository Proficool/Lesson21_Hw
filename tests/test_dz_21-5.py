import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_drag_and_drop(driver):
    driver.get("https://jqueryui.com/droppable/")

    # Переключаемся на iframe, содержащий элементы для перетаскивания
    iframe = driver.find_element(By.CSS_SELECTOR, ".demo-frame")
    driver.switch_to.frame(iframe)

    # Находим элементы для перетаскивания и область назначения
    draggable = driver.find_element(By.CSS_SELECTOR, "#draggable")
    droppable = driver.find_element(By.CSS_SELECTOR, "#droppable")

    # Выполняем перетаскивание
    actions = ActionChains(driver)
    actions.drag_and_drop(draggable, droppable).perform()
    time.sleep(10)
    # Проверяем, что текст изменился на "Dropped!"
    assert droppable.text == "Dropped!", f"Ожидался текст 'Dropped!', но получен '{droppable.text}'"