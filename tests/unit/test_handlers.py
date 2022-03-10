from pension_planner.domain import commands
from pension_planner.domain.commands import OpenAccount, UpdateAccountAttribute, CreateSingleOrder, CreateStandingOrder, \
    UpdateOrderAttribute


# TODO need to fake out frontend or change handlers to make this test pass
def test_open_bank_account(fake_bus):
    command = OpenAccount()
    [id_] = fake_bus.handle(command)
    assert fake_bus.uow.committed is True
    assert id_ is not None


def test_update_account_attribute(fake_bus):
    # setup account
    command = OpenAccount()
    [id_] = fake_bus.handle(command)
    command = UpdateAccountAttribute(
        id_=id_,
        attribute="name",
        new_value="Bankkonto #42"
    )
    fake_bus.handle(command)
    assert fake_bus.uow.committed is True
    account = fake_bus.uow.accounts.get(id_)
    assert account.name == "Bankkonto #42"


def test_close_account(fake_bus):
    # setup account
    command = OpenAccount()
    [id_] = fake_bus.handle(command)
    fake_bus.handle(commands.CloseAccount(id_=id_))
    assert fake_bus.uow.accounts.get(id_) is None


def test_place_single_order(fake_bus):
    command = CreateSingleOrder()
    [id_] = fake_bus.handle(command)
    assert fake_bus.uow.committed is True
    assert id_ is not None


def test_place_standing_order(fake_bus):
    command = CreateStandingOrder()
    [id_] = fake_bus.handle(command)
    assert fake_bus.uow.committed is True
    assert id_ is not None


def test_update_order_attribute(fake_bus):
    # setup account and order
    [account_id] = fake_bus.handle(OpenAccount())
    [order_id] = fake_bus.handle(CreateSingleOrder())
    command = UpdateOrderAttribute(
        id_=order_id,
        attribute="from_acc_id",
        new_value=account_id
    )
    fake_bus.handle(command)
    assert fake_bus.uow.committed is True
    order = fake_bus.uow.orders.get(order_id)
    assert order.from_acc_id == account_id
