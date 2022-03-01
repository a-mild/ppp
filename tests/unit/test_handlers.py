from typing import Any
from uuid import UUID

import pytest

from pension_planner.adapters.repositories import AbstractRepository, Entity
from pension_planner.bootstrap import bootstrap
from pension_planner.domain.account import Account
from pension_planner.domain.commands import OpenAccount, UpdateAccountAttribute
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class FakeAccountRepository(AbstractRepository):
    data: dict[UUID, Account] = {}

    def __init__(self):
        super().__init__()

    def _add(self, account: Account) -> None:
        id_ = account.id_
        self.data[id_] = account

    def _get(self, id_: UUID) -> Account:
        return self.data[id_]

    def _update(self, id_: UUID, attribute: str, new_value: Any) -> Entity:
        account = self.data.get(id_)
        if not account:
            return
        setattr(account, attribute, new_value)
        return account


class FakeUnitOfWork(AbstractUnitOfWork):

    def init_repositories(self) -> None:
        self._repos["accounts"] = FakeAccountRepository()

    def __enter__(self):
        self.committed = False
        return super().__enter__()

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


@pytest.fixture
def fake_uow():
    fake_uow = FakeUnitOfWork()
    yield fake_uow
    # reset data for next test
    fake_uow.accounts.data = {}


@pytest.fixture
def bus(fake_uow):
    dependencies = {
        AbstractUnitOfWork: fake_uow
    }
    return bootstrap(
        start_orm=False,
        dependencies=dependencies
    )


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
