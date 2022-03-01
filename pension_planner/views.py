from dataclasses import asdict
from typing import Any
from uuid import UUID

from sqlalchemy import select

from pension_planner.domain.account import Account
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


def account_data(id_: UUID, uow: SQLAlchemyUnitOfWork) -> dict[str, Any]:
    with uow:
        stmt = select(Account).filter_by(id_=id_)
        [account] = uow.session.execute(stmt).one_or_none()
        return {"id_": str(account.id_),
                "name": account.name,
                "interest_rate": account.interest_rate}
