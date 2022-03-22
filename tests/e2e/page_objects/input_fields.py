from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear(input_element: WebElement):
    input_element.send_keys(Keys.CONTROL, "a")
    input_element.send_keys(Keys.DELETE)


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


class SelectInputField:

    def __init__(self, locator):
        self.locator = locator
        self.current_id = 0

    def __set__(self, instance, value: int):
        active_tab_item: WebElement = instance.parent
        input_element = active_tab_item.find_element(*self.locator)
        driver: WebDriver = input_element.parent
        # open dropdown
        input_element.find_element(By.XPATH, "../..").find_element(By.TAG_NAME, "i").click()
        v_list_id = input_element.find_element(By.XPATH, "../../..").get_attribute("aria-owns")
        option_list: WebElement = (WebDriverWait(driver, 10)
                                   .until(EC.presence_of_element_located((By.ID, v_list_id))))
        options: list[WebElement] = option_list.find_elements(By.CLASS_NAME, "v-list-item")
        options[value].click()

    def __get__(self, instance, owner):
        active_tab_item: WebElement = instance.parent
        input_element = active_tab_item.find_element(*self.locator)
        parent = input_element.find_element(By.XPATH, "..")
        return parent.text


class SelectOptions:

    def __init__(self, input_field_locator):
        self.input_field_locator = input_field_locator

    def __get__(self, instance, owner) -> list[str]:
        input_element = instance.parent.find_element(*self.input_field_locator)
        driver: WebDriver = input_element.parent
        # open dropdown
        dd_btn = input_element.find_element(By.XPATH, "../..").find_element(By.TAG_NAME, "i")
        dd_btn.click()
        # find options list
        v_list_id = input_element.find_element(By.XPATH, "../../..").get_attribute("aria-owns")
        option_list: WebElement = (WebDriverWait(driver, 10)
                                   .until(EC.presence_of_element_located((By.ID, v_list_id))))
        # get options
        options = [list_item.text for list_item in
                   option_list.find_elements(By.CLASS_NAME, "v-list-item")]
        # close dropdown again
        dd_btn.click()
        return options
