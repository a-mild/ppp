from datetime import date
from typing import Union, Any, Callable
from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from pension_planner.adapters import orm
from pension_planner.adapters.repositories import AbstractRepository
from pension_planner.bootstrap import bootstrap
from pension_planner.domain import events
from pension_planner.domain.account import Account
from pension_planner.domain.orders import SingleOrder, StandingOrder, OrderBase
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    orm.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_sqlite_db):
    return sessionmaker(
        bind=in_memory_sqlite_db,
        future=True,
        expire_on_commit=False
    )


@pytest.fixture
def mappers():
    clear_mappers()
    orm.start_mappers()
    yield
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


Entity = Union[Account, OrderBase]


class FakeRepository(AbstractRepository):
    data: dict[UUID, Entity] = {}

    def __init__(self):
        super().__init__()

    def _add(self, entity: Entity) -> None:
        id_ = entity.id_
        self.data[id_] = entity

    def _get(self, id_: UUID) -> Entity:
        return self.data.get(id_, None)

    def _delete(self, id_: UUID) -> Entity | None:
        return self.data.pop(id_, None)

    def _update(self, id_: UUID, attribute: str, new_value: Any) -> Entity:
        entity = self.data.get(id_)
        if not entity:
            return
        setattr(entity, attribute, new_value)
        if isinstance(entity, OrderBase):
            event = events.OrderAttributeUpdated(id_=id_, attribute=attribute, new_value=new_value)
            entity.events.append(event)
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


@pytest.fixture
def account_factory():
    def _make_account():
        return Account(
            name="Girokonto #1",
            interest_rate=0.0,
        )
    return _make_account

@pytest.fixture
def single_order_factory():
    def _make_single_order(
            from_acc_id=None, target_acc_id=None,
            date_=date.today(),
            amount=0.0
    ) -> SingleOrder:
        return SingleOrder(
            name="Einzelauftrag #1",
            from_acc_id=from_acc_id,
            target_acc_id=target_acc_id,
            date=date_,
            amount=amount
        )
    return _make_single_order


@pytest.fixture
def standing_order_factory():
    def _make_standing_order(
            from_acc_id=None, target_acc_id=None,
            start_date=date(2022, 1, 1), end_date=date(2022, 12, 1),
            amount=100.0
    ) -> StandingOrder:
        return StandingOrder(
            name="Dauerauftrag #1",
            from_acc_id=from_acc_id,
            target_acc_id=target_acc_id,
            start_date=start_date,
            end_date=end_date,
            amount=amount
        )
    return _make_standing_order
