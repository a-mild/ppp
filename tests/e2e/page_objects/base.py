from selenium.webdriver.remote.webdriver import BaseWebDriver
from selenium.webdriver.remote.webelement import BaseWebElement
from selenium.webdriver.support.wait import WebDriverWait


ELEMENT_WAIT_TIME = 10


class BasePage:

    def __init__(self, driver: BaseWebDriver) -> None:
        self.driver = driver



class BasePageElement:

    def __init__(self, locator) -> None:
        self.locator = locator

    def __get__(self, obj, owner) -> BaseWebElement:
        driver = obj.driver
        elem: BaseWebElement = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(self.locator)
        return elem
