import pytest
import logging
import signal
import subprocess
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.e2e.page_objects.app import MainPage


@pytest.fixture
def driver(test_dir):
    geckodriver_path = test_dir / "geckodriver.exe"
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    yield driver
    driver.close()


@pytest.fixture
def run_voila(test_notebook_path, driver):
    process = subprocess.Popen(f"voila {test_notebook_path} --no-browser",
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)

    try:
        driver.get("http://localhost:8866/")
        WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "v-toolbar__title"),
                                             text_="Pa's Pension Planner"))
        yield
    except WebDriverException as err:
        logging.error(err)
        driver.quit()
    process.send_signal(signal.CTRL_BREAK_EVENT)
    process.kill()


@pytest.fixture
def main_page(driver):
    return MainPage(driver)
