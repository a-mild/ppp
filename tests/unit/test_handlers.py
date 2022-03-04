from pension_planner.domain import commands
from pension_planner.domain.commands import OpenAccount, UpdateAccountAttribute, CreateSingleOrder, CreateStandingOrder, \
    UpdateOrderAttribute


# TODO need to fake out frontend or change handlers to make this test pass
def test_open_bank_account(bus):
    command = OpenAccount()
    [id_] = bus.handle(command)
    assert bus.uow.committed is True
    assert id_ is not None


def test_update_account_attribute(bus):
    # setup account
    command = OpenAccount()
    [id_] = bus.handle(command)
    command = UpdateAccountAttribute(
        id_=id_,
        attribute="name",
        new_value="Bankkonto #42"
    )
    bus.handle(command)
    assert bus.uow.committed is True
    account = bus.uow.accounts.get(id_)
    assert account.name == "Bankkonto #42"


def test_close_account(bus):
    # setup account
    command = OpenAccount()
    [id_] = bus.handle(command)
    bus.handle(commands.CloseAccount(id_=id_))
    assert bus.uow.accounts.get(id_) is None


def test_place_single_order(bus):
    command = CreateSingleOrder()
    [id_] = bus.handle(command)
    assert bus.uow.committed is True
    assert id_ is not None


def test_place_standing_order(bus):
    command = CreateStandingOrder()
    [id_] = bus.handle(command)
    assert bus.uow.committed is True
    assert id_ is not None


def test_update_order_attribute(bus):
    # setup account and order
    [account_id] = bus.handle(OpenAccount())
    [order_id] = bus.handle(CreateSingleOrder())
    command = UpdateOrderAttribute(
        id_=order_id,
        attribute="from_acc_id",
        new_value=account_id
    )
    bus.handle(command)
    assert bus.uow.committed is True
    order = bus.uow.orders.get(order_id)
    assert order.from_acc_id == account_id
