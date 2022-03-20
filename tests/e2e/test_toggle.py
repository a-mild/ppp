import pytest

from tests.e2e.page_objects.app import MainPage

pytestmark = pytest.mark.usefixtures("run_voila")


def test_toggle(driver):
    page = MainPage(driver)
    page.toggle_sidebar()
