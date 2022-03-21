from selenium.webdriver.remote.webelement import WebElement



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


