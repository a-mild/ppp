from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


from tests.e2e.page_objects.base import BasePage, BasePageElement
from tests.e2e.page_objects.input_fields import TextInputField


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
        active_tab_item = self.tabs_items_accounts.find_element(By.CLASS_NAME, "v-window-item--active")
        return AccountController(active_tab_item)

    def __len__(self):
        return len(self.tabs)

    def delete(self, item: int) -> None:
        self.tabs[item].find_element(By.TAG_NAME, "button").click()


class AccountsTab(BasePage):
    btn_open_account = BasePageElement(EC.element_to_be_clickable((By.ID, "open_account")))
    tabs_accounts = BasePageElement(EC.presence_of_element_located((By.ID, "tabs-accounts")))
    tabs_items_accounts = BasePageElement(EC.presence_of_element_located((By.ID, "tabs-items-accounts")))

    def open_account(self):
        self.btn_open_account.click()

    @property
    def accounts(self):
        return AccountsList(self.tabs_accounts, self.tabs_items_accounts)
