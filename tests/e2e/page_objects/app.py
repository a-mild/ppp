from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from tests.e2e.page_objects.account_tab import AccountsTab
from tests.e2e.page_objects.base import BasePage, BasePageElement
from tests.e2e.page_objects.orders_tab import OrdersTab


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
