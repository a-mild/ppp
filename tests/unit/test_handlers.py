from pension_planner.domain.commands import OpenAccount, UpdateAccountAttribute, CreateSingleOrder, CreateStandingOrder


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
