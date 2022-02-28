from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from pension_planner.domain.account import Account
from pension_planner.service_layer.unit_of_work import SQLAlchemyAccountsUnitOfWork, SQLAlchemyOrdersUnitOfWork


def test_uow_can_insert_account(session_factory, base_account):
    uow = SQLAlchemyAccountsUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(base_account)

    stmt = text("SELECT * FROM accounts")
    with session_factory() as session:
        result = session.execute(stmt).all()
        assert len(result) > 0

def test_uow_can_get_backrefs(session_factory, base_account, single_order):
    id_ = base_account.id_
    uow_accounts = SQLAlchemyAccountsUnitOfWork(session_factory)
    uow_orders = SQLAlchemyOrdersUnitOfWork(session_factory)
    with uow_accounts:
        uow_accounts.accounts.add(base_account)
    with uow_orders:
        uow_orders.orders.add(single_order)
    with uow_accounts:
        acc = uow_accounts.accounts.get(id_)
    assert acc is not None
    assert acc.assets == [single_order]


