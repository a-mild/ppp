from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from pension_planner.domain.account import Account
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


def test_uow_can_insert_account(session_factory, account: Account):
    uow = SQLAlchemyUnitOfWork(session_factory)
    with uow:
        uow.accounts.add(account)

    stmt = text("SELECT * FROM account")
    with session_factory() as session:
        result = session.execute(stmt).all()
        assert len(result) > 0


