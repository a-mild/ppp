from typing import Any, Union
from uuid import UUID

import pytest

from pension_planner.adapters.repositories import AbstractRepository
from pension_planner.bootstrap import bootstrap
from pension_planner.domain.account import Account
from pension_planner.domain.commands import OpenAccount, UpdateAccountAttribute, CreateSingleOrder, CreateStandingOrder
from pension_planner.domain.events import OrderCreated, AccountOpened
from pension_planner.domain.orders import OrderBase
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


Entity = Union[Account, OrderBase]


class FakeRepository(AbstractRepository):
    data: dict[UUID, Entity] = {}

    def __init__(self):
        super().__init__()

    def _add(self, entity: Entity) -> None:
        id_ = entity.id_
        if isinstance(entity, Account):
            self.data[id_] = entity
        elif isinstance(entity, OrderBase):
            self.data[id_] = entity

    def _get(self, id_: UUID) -> Entity:
        return self.data[id_]

    def _update(self, id_: UUID, attribute: str, new_value: Any) -> Entity:
        entity = self.data.get(id_)
        if not entity:
            return
        setattr(entity, attribute, new_value)
        return entity


class FakeUnitOfWork(AbstractUnitOfWork):

    def init_repositories(self) -> None:
        repo = FakeRepository()
        self._repos["accounts"] = repo
        self._repos["orders"] = repo

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
