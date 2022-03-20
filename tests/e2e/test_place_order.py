import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pension_planner.domain.orders import ORDER_TYPES

pytestmark = pytest.mark.usefixtures("run_voila")


def test_can_create_an_order(main_page):
    # the user opens the orders tab in the side drawer
    sidebar = main_page.toggle_sidebar()
    tab = sidebar.open_orders_tab()
    assert "active" in sidebar.orders_tab.get_attribute("class")
    # he clicks on the button to place a new order and creates a single order
    tab.place_single_order()
    # he gets to see input fields for all the parameters


    # order_editor = tab_item_orders.find_element(By.ID, "order_editor")
    # for id_ in ["name", "from_acc_id", "target_acc_id", "date", "amount"]:
    #     widget = order_editor.find_element(By.ID, id_)
