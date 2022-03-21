import time
from collections import UserDict, UserList
from typing import Union, TypeVar

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ELEMENT_WAIT_TIME = 10

def clear(input_element: WebElement):
    input_element.send_keys(Keys.CONTROL, "a")
    input_element.send_keys(Keys.DELETE)


class BasePage:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver


class WebElementWrapper:

    def __init__(self, wrapped_element: WebElement) -> None:
        self.wrapped_element = wrapped_element

    def __getattr__(self, item):
        return getattr(self.wrapped_element, item)


WrappedElement = TypeVar("WrappedElement")


class BasePageElement:

    def __init__(self, locator, wrapper: WrappedElement = None) -> None:
        self.locator = locator
        self.wrapper = wrapper

    def __get__(self, obj, owner) -> Union[WebElement, WrappedElement]:
        driver = obj.driver
        elem: WebElement = WebDriverWait(driver, ELEMENT_WAIT_TIME).until(self.locator)
        if self.wrapper is None:
            return elem
        return self.wrapper(elem)


class TextInputField:

    def __init__(self, locator):
        self.locator = locator

    def __set__(self, instance, value):
        parent: WebElement = instance.parent
        input_element = parent.find_element(*self.locator)
        clear(input_element)
        input_element.send_keys(value)
        input_element.send_keys(Keys.ENTER)

    def __get__(self, obj, owner):
        parent: WebElement = obj.parent
        input_element = parent.find_element(*self.locator)
        return input_element.get_property("value")


class AccountController:
    account_name = TextInputField((By.ID, "account_name"))
    interest_rate = TextInputField((By.ID, "interest_rate"))

    def __init__(self, parent: WebElement) -> None:
        self.parent = parent


class AccountsList:

    def __init__(self, tabs_accounts: WebElement, tabs_items_accounts: WebElement) -> None:
        self.tabs_accounts = tabs_accounts
        self.tabs_items_accounts = tabs_items_accounts

    @property
    def tabs(self) -> list[WebElement]:
        return self.tabs_accounts.find_elements(By.CLASS_NAME, "v-tab")

    def __getitem__(self, item):
        self.tabs[item].click()
        web_element = self.tabs_items_accounts.find_element(By.CLASS_NAME, "v-window-item--active")
        return AccountController(web_element)

    def __len__(self):
        return len(self.tabs)

    def delete(self, item: int) -> None:
        self.tabs[item].find_element(By.TAG_NAME, "button").click()


class AccountsTab(BasePage):
    btn_open_account = BasePageElement(EC.element_to_be_clickable((By.ID, "open_account")))
    tabs_accounts = BasePageElement(EC.presence_of_element_located((By.ID, "tabs-accounts")))
    tabs_items_accounts = BasePageElement(EC.presence_of_element_located((By.ID, "tabs-items-accounts")))

    def __init__(self, driver):
        super().__init__(driver)

    def open_account(self):
        self.btn_open_account.click()

    @property
    def accounts(self):
        return AccountsList(self.tabs_accounts, self.tabs_items_accounts)


class OrdersTab(BasePage):
    btn_place_order = BasePageElement(EC.element_to_be_clickable((By.ID, "place_order_btn")))
    div_single_order = BasePageElement(EC.element_to_be_clickable((By.ID, "SingleOrder")))
    div_standing_order = BasePageElement(EC.element_to_be_clickable((By.ID, "StandingOrder")))

    def place_single_order(self):
        self.btn_place_order.click()
        self.div_standing_order.click()

    def place_standing_order(self):
        self.btn_place_order.click()
        self.div_standing_order.click()


class Sidebar(BasePage):
    accounts_tab = BasePageElement(EC.element_to_be_clickable((By.ID, "accounts_tab")))
    orders_tab = BasePageElement(EC.element_to_be_clickable((By.ID, "orders_tab")))
    accounts_tab_item = BasePageElement(EC.presence_of_element_located((By.ID, "tab-item-accounts")))
    # orders_tab_item = BasePageElement(EC.presence_of_element_located((By.ID, "tab-item-orders")))

    def open_accounts_tab(self) -> AccountsTab:
        self.accounts_tab.click()
        return AccountsTab(self.driver)

    def open_orders_tab(self):
        self.orders_tab.click()
        return OrdersTab(self.driver)


class MainPage(BasePage):
    toggle_sidebar_btn = BasePageElement(EC.element_to_be_clickable((By.ID, "toggle_sidebar_button")))

    def toggle_sidebar(self) -> Sidebar:
        self.toggle_sidebar_btn.click()
        return Sidebar(self.driver)
