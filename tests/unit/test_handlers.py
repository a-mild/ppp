import logging
from datetime import date

from pension_planner.domain import commands
from pension_planner.domain.commands import OpenAccount, UpdateAccountAttribute, CreateSingleOrder, CreateStandingOrder, \
    UpdateOrderAttribute, DeleteOrder


# TODO need to fake out frontend or change handlers to make this test pass
def test_open_bank_account(fake_bus):
    command = OpenAccount()
    [id_] = fake_bus.handle(command)
    assert fake_bus.uow.committed is True
    assert id_ is not None


def test_close_account(fake_bus):
    # setup account
    command = OpenAccount()
    [id_] = fake_bus.handle(command)
    fake_bus.handle(commands.CloseAccount(id_=id_))
    assert fake_bus.uow.accounts.get(id_) is None


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


def test_delete_order(fake_bus):
    [id_] = fake_bus.handle(CreateStandingOrder())

    fake_bus.handle(DeleteOrder(id_=id_))

    assert fake_bus.uow.orders.get(id_) is None


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


def test_update_plotting_frontend(
        fake_bus, fake_frontend, single_order_factory, standing_order_factory):
    single_order_1 = single_order_factory(
        date_=date(2021, 12, 1),
        amount=2400
    )
    command = commands.OpenAccount(
        interest_rate=0.0,
        assets=[single_order_1],
        liabilities=[]
    )
    fake_bus.handle(command)
    # assert fake_frontend.x == [date(2021, 12, 1)]
    assert fake_frontend.y == [0, 2400]
    # standing_order_1 = standing_order_factory(
    #     start_date=date(2020, 1, 1),
    #     end_date=date(2020, 12, 1),
    #     amount=100
    # )
    # standing_order_2 = standing_order_factory(
    #     start_date=date(2021, 1, 1),
    #     end_date=date(2021, 12, 1),
    #     amount=100
    # )
    # single_order_2 = single_order_factory(
    #     date_=date(2022, 12, 1),
    #     amount=3000
    # )
    # standing_order_3 = standing_order_factory(
    #     start_date=date(2018, 1, 1),
    #     end_date=date(2020, 12, 1),
    #     amount=200
    # )
    # standing_order_4 = standing_order_factory(
    #     start_date=date(2019, 1, 1),
    #     end_date=date(2020, 12, 1),
    #     amount=50
    # )
    #
    # open_account_1 = commands.OpenAccount(
    #     interest_rate=0.1,
    #     assets=[standing_order_1, standing_order_2],
    #     liabilities=[single_order_1],
    # )
    # open_account_2 = commands.OpenAccount(
    #     interest_rate=0.05,
    #     assets=[standing_order_3, standing_order_4],
    #     liabilities=[single_order_2],
    # )
    # fake_bus.handle(open_account_1)
    # fake_bus.handle(open_account_2)
