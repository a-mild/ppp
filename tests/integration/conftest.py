import pytest

from pension_planner.adapters.repositories import SQLAlchemyAccountRepository, SQLAlchemyOrderRepository


@pytest.fixture
def sa_account_repo(session):
    return SQLAlchemyAccountRepository(session)


@pytest.fixture
def sa_order_repo(session):
    return SQLAlchemyOrderRepository(session)
