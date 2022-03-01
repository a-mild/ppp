import pytest
from pension_planner.adapters.repositories import SQLAlchemyAccountRepository, SQLAlchemyOrderRepository


def test_add_account(session, base_account):
    repo = SQLAlchemyAccountRepository(session)
    repo.add(base_account)
    assert repo.get(base_account.id_) == base_account


def test_add_orders(session, base_account, single_order, standing_order):
    accounts_repo = SQLAlchemyAccountRepository(session)
    accounts_repo.add(base_account)
    orders_repo = SQLAlchemyOrderRepository(session)
    orders_repo.add(single_order)
    orders_repo.add(standing_order)
    assert orders_repo.get(single_order.id_) == single_order
    assert orders_repo.get(standing_order.id_) == standing_order

def test_orders_backref(session, base_account, single_order, standing_order):
    accounts_repo = SQLAlchemyAccountRepository(session)
    accounts_repo.add(base_account)
    orders_repo = SQLAlchemyOrderRepository(session)
    orders_repo.add(single_order)
    orders_repo.add(standing_order)
    session.commit()
    acc = accounts_repo.get(base_account.id_)
    assert acc.assets == [single_order, standing_order]

def test_update_account(session, base_account):
    id_ = base_account.id_
    accounts_repo = SQLAlchemyAccountRepository(session)
    accounts_repo.add(base_account)
    session.commit()
    accounts_repo.update(id_, "name", "Girokonto #42")
    accounts_repo.update(id_, "interest_rate", 0.001)
    session.commit()
    revived = accounts_repo.get(id_)
    assert revived.name == "Girokonto #42"
    assert revived.interest_rate == 0.001
