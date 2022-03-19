import logging
import signal
import subprocess
import time
from typing import Callable

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

import pytest


def wait_for(assertion: Callable, max_wait: int = 10) -> None:
    start_time = time.time()
    while True:
        try:
            return assertion()
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > max_wait:
                raise e
            time.sleep(0.5)


@pytest.fixture
def driver(test_dir):
    geckodriver_path = test_dir / "geckodriver.exe"
    driver = webdriver.Firefox(executable_path=geckodriver_path)
    yield driver
    driver.close()


@pytest.fixture
def run_voila(test_notebook_path, driver):
    process = subprocess.Popen(f"voila {test_notebook_path} --no-browser", creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    driver.get("http://localhost:8866/")

    def assertion():
        assert "Pa's Pension Planner" in driver.find_element(By.CLASS_NAME, "v-toolbar__title").text

    wait_for(assertion, max_wait=20)
    yield
    time.sleep(10)
    process.send_signal(signal.CTRL_BREAK_EVENT)
    process.kill()


@pytest.fixture
def open_drawer(driver):
    driver.find_element(By.ID, "toggle_sidebar_button").click()
