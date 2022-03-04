from datetime import date
from typing import Union, Any
from uuid import UUID

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from pension_planner.adapters.orm import metadata, start_mappers
from pension_planner.adapters.repositories import AbstractRepository
from pension_planner.bootstrap import bootstrap
from pension_planner.domain import events
from pension_planner.domain.account import Account
from pension_planner.domain.orders import SingleOrder, StandingOrder, OrderBase
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_sqlite_db):
    clear_mappers()
    start_mappers()
    yield sessionmaker(bind=in_memory_sqlite_db, future=True, expire_on_commit=False)
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
def base_account() -> Account:
    return Account(
        name="Girokonto #1",
        interest_rate=0.0,
        assets=list(),
        liabilities=list()
    )

@pytest.fixture
def single_order(base_account) -> SingleOrder:
    return SingleOrder(
        name="Einzelauftrag #1",
        target_acc_id=None,
        from_acc_id=base_account.id_,
        date=date(2021, 12, 1),
        amount=1200.0
    )


@pytest.fixture
def standing_order(base_account) -> StandingOrder:
    return StandingOrder(
        name="Dauerauftrag #1",
        target_acc_id=base_account.id_,
        from_acc_id=None,
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 1),
        amount=100.0
    )
