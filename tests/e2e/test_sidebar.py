import pytest

from pension_planner import views
from src.pension_planner.domain import OpenAccount, CreateSingleOrder, UpdateOrderAttribute
from src.pension_planner.domain import ORDER_ATTRIBUTES
from src.pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_accounts.tab_item_accounts import TabItemAccounts
from src.pension_planner.frontend.ipyvuetify.components.sidebar.tab_item_orders.order_editor import OrderEditor
from src.pension_planner.frontend import TabItemOrders
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


def test_order_editor():
    order_editor = OrderEditor()
    assert all(order_editor.has_trait(attr) for attr in ORDER_ATTRIBUTES)


def test_update_dropdown():
    editor = THE_APP.sidebar.tab_item_orders.order_editor
    assert editor.from_acc_id.value is None
    assert editor.from_acc_id.options == (("", None),)
    assert editor.target_acc_id.value is None
    assert editor.target_acc_id.options == (("", None),)
    bus.handle(OpenAccount())
    bus.handle(CreateSingleOrder())
    accounts = views.fetch_all_accounts(bus.uow)
    options = (("", None),) + tuple((name, id_) for name, id_ in accounts.items())
    assert editor.from_acc_id.value is None
    assert editor.from_acc_id.options == options
    assert editor.target_acc_id.value is None
    assert editor.target_acc_id.options == options
    # select an account
    editor.from_acc_id.value = options[1][1]
    assert editor.from_acc_id.options == options
    assert editor.target_acc_id.options == (("", None),)
    # revert selection
    editor.from_acc_id.value = None
    assert editor.target_acc_id.options == options
    # other way around
    editor.target_acc_id.value = options[1][1]
    assert editor.target_acc_id.options == options
    assert editor.from_acc_id.options == (("", None),)
    # revert selection
    editor.target_acc_id.value = None
    assert editor.from_acc_id.options == options
    # set one and add another account
    editor.target_acc_id.value = options[1][1]
    bus.handle(OpenAccount())
    assert editor.target_acc_id.value == options[1][1]
    assert editor.from_acc_id.value is None


def test_overview():
    overview = THE_APP.sidebar.tab_item_orders.overview
    [acc_id] = bus.handle(OpenAccount())
    assert str(acc_id) in overview.accounts
    [order_id] = bus.handle(CreateSingleOrder())
    order = views.fetch_order(order_id, bus.uow)
    # assign to an account
    bus.handle(UpdateOrderAttribute(order_id, "from_acc_id", acc_id))
    assert str(order_id) in overview.accounts[str(acc_id)].liabilities
    card = overview.accounts[str(acc_id)].liabilities[str(order_id)]
    assert card.id_ == order["id_"]
    assert card.name == order["name"]
    # revert
    bus.handle(UpdateOrderAttribute(order_id, "from_acc_id", None))


