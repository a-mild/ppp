import pytest

from pension_planner.frontend.components.sidebar import TabItemAccounts, TabItemOrders
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


@pytest.fixture
def tab_item_accounts() -> TabItemAccounts:
    return TabItemAccounts()


@pytest.fixture
def tab_item_orders() -> TabItemOrders:
    return TabItemOrders()


def test_open_account(tab_item_accounts):
    tab_item_accounts.vue_open_account()
    assert len(tab_item_accounts.accounts) > 0


def test_place_order(tab_item_orders, session_factory, base_account, single_order):
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(base_account)
        uow.orders.add(single_order)
    change = {"new": str(single_order.id_)}
    tab_item_orders.on_order_id_changed(change, uow)
    assert tab_item_orders.amount.v_model == single_order.amount
