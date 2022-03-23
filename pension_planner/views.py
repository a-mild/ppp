from dataclasses import asdict
from typing import Any, Union
from uuid import UUID

from sqlalchemy import select

from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase, SingleOrder, StandingOrder
from pension_planner.service_layer.unit_of_work import SQLAlchemyUnitOfWork


def fetch_account(id_: UUID, uow: SQLAlchemyUnitOfWork) -> dict[str, Any]:
    with uow:
        stmt = select(Account).filter_by(id_=id_)
        [account] = uow.session.execute(stmt).one_or_none()
        return {"id_": account.id_,
                "name": account.name,
                "interest_rate": account.interest_rate}


def fetch_all_accounts(uow: SQLAlchemyUnitOfWork) -> list[tuple[UUID, str]]:
    with uow:
        stmt = select(Account.id_, Account.name)
        accounts = uow.session.execute(stmt).all()
        return list(accounts)


def fetch_order(id_: UUID, uow: SQLAlchemyUnitOfWork) -> dict[str, Any]:
    with uow:
        stmt = (select(OrderBase)
                .filter_by(id_=id_)
                .options())
        order = uow.session.execute(stmt).scalars().first()
        result = asdict(order) | {"type": order.type}
        return result
