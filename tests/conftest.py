from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from pension_planner.adapters.orm import metadata, start_mappers
from pension_planner.domain.account import Account
from pension_planner.domain.orders import SingleOrder, StandingOrder


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    metadata.create_all(engine)
    return engine

@pytest.fixture
def session_factory(in_memory_sqlite_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_sqlite_db, future=True, expire_on_commit=False)
    clear_mappers()

@pytest.fixture
def session(session_factory):
    return session_factory()


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
        target_acc_id=base_account.id_,
        from_acc_id=None,
        date=date(2022, 12, 1),
        amount=100.0
    )


@pytest.fixture
def standing_order(base_account) -> StandingOrder:
    return StandingOrder(
        name="Dauerauftrag #1",
        target_acc_id=base_account.id_,
        from_acc_id=None,
        start_date=date(2021, 1, 1),
        end_date=date(2022, 1, 1),
        amount=100.0
    )
