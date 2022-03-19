import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


pytestmark = pytest.mark.usefixtures("run_voila")


def test_open_account(driver, open_drawer):
    # The User sees the control panel for opening accounts
    tab_item_accounts = (WebDriverWait(driver, 30)
                         .until(EC.presence_of_element_located((By.ID, "tab-item_accounts")))
                         )
    # The user clicks on the "open account" button
    button = (WebDriverWait(driver, 30)
              .until(EC.element_to_be_clickable((By.ID, "open_account")))
              )
    button.click()
    # he gets to see input fields for the name of the account and its interest rate
    input_fields: list[WebElement] = tab_item_accounts.find_elements(by=By.CLASS_NAME, value="v-input")
    assert len(input_fields) == 2
    assert "Kontoname" in input_fields[0].text
    assert "Zinsen" in input_fields[1].text

    # and the new account is listed at the bottom
    tabs = tab_item_accounts.find_elements(by=By.CLASS_NAME, value="v-tab")

    assert len(tabs) == 1
    assert "Konto #1" in tabs[0].text
