from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from pension_planner.adapters.orm import metadata, start_mappings
from pension_planner.domain.account import Account
from pension_planner.domain.orders import SingleOrder, StandingOrder


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    metadata.create_all(engine)
    return engine

@pytest.fixture
def session_factory(in_memory_sqlite_db):
    start_mappings()
    yield sessionmaker(bind=in_memory_sqlite_db, future=True)
    clear_mappers()

@pytest.fixture
def session(session_factory):
    return session_factory()


@pytest.fixture
def account():
    return Account(
        name="Girokonto #1",
        interest_rate=0.0,
        orders=[]
    )

@pytest.fixture
def single_order() -> SingleOrder:
    name = "single payment"
    side = BalanceSheetSide.asset
    ts = date(2022, 12, 1)
    amount = 100.00
    return SingleOrder(name=name, side=side, timestamp=ts, amount=amount)



@pytest.fixture
def constant_payment() -> StandingOrder:
    name = "constant payment"
    side = BalanceSheetSide.asset
    from_ts = date(2021, 1, 1)
    until_ts = date(2022, 1, 1)
    amount = 100
    return StandingOrder(name=name, side=side, from_ts=from_ts, until_ts=until_ts, amount=amount)
