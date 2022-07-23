import pytest

from src.pension_planner.adapters.repositories import SQLAlchemyAccountRepository, SQLAlchemyOrderRepository
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


@pytest.fixture
def sa_account_repo(session):
    return SQLAlchemyAccountRepository(session)


@pytest.fixture
def sa_order_repo(session):
    return SQLAlchemyOrderRepository(session)


@pytest.fixture
def sa_uow(session_factory):
    return SQLAlchemyUnitOfWork(session_factory)