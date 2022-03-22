from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.e2e.page_objects.base import BasePage, BasePageElement
from tests.e2e.page_objects.input_fields import TextInputField, SelectInputField, SelectOptions


class OrderController:
    name = TextInputField((By.ID, "name"))
    from_acc = SelectInputField((By.ID, "from-acc-select"))
    from_acc_options = SelectOptions((By.ID, "from-acc-select"))
    target_acc = SelectInputField((By.ID, "target-acc-select"))
    target_acc_options = SelectOptions((By.ID, "target-acc-select"))
    date = TextInputField((By.ID, "date"))
    amount = TextInputField((By.ID, "amount"))

    def __init__(self, parent: WebElement) -> None:
        self.parent = parent



class OrdersList:

    def __init__(self, tabs_orders: WebElement, tabs_items_orders: WebElement) -> None:
        self.tabs_orders = tabs_orders
        self.tabs_items_orders = tabs_items_orders

    @property
    def tabs(self) -> list[WebElement]:
        return self.tabs_orders.find_elements(By.CLASS_NAME, "v-tab")

    def __getitem__(self, item: int) -> OrderController:
        self.tabs[item].click()
        active_tab_item = self.tabs_items_orders.find_element(By.CLASS_NAME, "v-window-item--active")
        return OrderController(active_tab_item)

    def __len__(self):
        return len(self.tabs)

    def delete(self, item: int) -> None:
        self.tabs[item].find_element(By.TAG_NAME, "button").click()


class OrdersTab(BasePage):
    btn_place_order = BasePageElement(EC.element_to_be_clickable((By.ID, "place_order_btn")))
    div_single_order = BasePageElement(EC.element_to_be_clickable((By.ID, "SingleOrder")))
    div_standing_order = BasePageElement(EC.element_to_be_clickable((By.ID, "StandingOrder")))

    tabs_orders = BasePageElement(EC.presence_of_element_located((By.ID, "tabs-orders")))
    tabs_items_orders = BasePageElement(EC.presence_of_element_located((By.ID, "tabs-items-orders")))

    def place_single_order(self):
        self.btn_place_order.click()
        self.div_single_order.click()

    def place_standing_order(self):
        self.btn_place_order.click()
        self.div_standing_order.click()

    @property
    def orders(self):
        return OrdersList(self.tabs_orders, self.tabs_items_orders)
