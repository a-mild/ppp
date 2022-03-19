import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


pytestmark = pytest.mark.usefixtures("run_voila")


def test_can_create_an_order(driver, open_drawer):
    # the user opens the orders tab in the side drawer
    orders_tab = (WebDriverWait(driver, 30)
                  .until(EC.presence_of_element_located((By.ID, "orders_tab")))
                  )
    orders_tab.click()
    tab_item_orders: WebElement = (WebDriverWait(driver, 30)
                       .until(EC.presence_of_element_located((By.ID, "tab-item-orders")))
                       )
    # the users sees two buttons to create either a single order or a standing order
    place_orders_div: WebElement = (WebDriverWait(driver, 30)
                                    .until(EC.presence_of_element_located((By.ID, "place_order_buttons")))
                                    )
    order_buttons = place_orders_div.find_elements(by=By.TAG_NAME, value="button")
    assert len(order_buttons) == 2

    # the user clicks on the button that creates a single order
    so_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "SingleOrder")))
    # so_button = place_orders_div.find_element(By.ID, "SingleOrder")
    so_button.click()
    # ... and sees input fields for the parameters
    order_editor = tab_item_orders.find_element(By.ID, "order_editor")
    for id_ in ["name", "from_acc_id", "target_acc_id", "date", "amount"]:
        widget = order_editor.find_element(By.ID, id_)
