import time

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
    # Currently there are no orders
    assert len(tab.orders) == 0
    # he clicks on the button to place a new order and creates a single order
    tab.place_single_order()
    # he gets to see input fields for all the parameters
    controller = tab.orders[0]
    assert "Einzelauftrag" in controller.name
    assert controller.from_acc == "Hallo"
    assert controller.from_acc_options == ["Hallo", "Welt"]
    assert controller.target_acc == "hallo"
    assert controller.target_acc_options == ["hallo", "welt"]
    assert controller.date == "2022-03"
    assert controller.amount == "100"


def test_can_delete_order(main_page):
    # The user creates an order
    sidebar = main_page.toggle_sidebar()
    tab = sidebar.open_orders_tab()
    tab.place_single_order()

    # and deletes it again
    tab.orders.delete(0)

    # so there are no more orders
    assert len(tab.orders) == 0
