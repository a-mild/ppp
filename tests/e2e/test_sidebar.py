import pytest

from pension_planner.frontend.components.sidebar import TabItemAccounts, TabItemOrders


@pytest.fixture
def tab_item_accounts() -> TabItemAccounts:
    return TabItemAccounts()

@pytest.fixture
def tab_item_orders() -> TabItemOrders:
    return TabItemOrders()


def test_open_account(tab_item_accounts):
    tab_item_accounts.vue_open_account()
    assert len(tab_item_accounts.accounts) > 0


def test_place_order(tab_item_orders):
    tab_item_orders.vue_place_order("SingleOrder")
    assert tab_item_orders.output != ""
