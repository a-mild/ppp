from abc import ABC, abstractmethod
from typing import TypeVar, Any
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session, joinedload

from pension_planner.adapters.orm import orders_table
from pension_planner.domain import events
from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase

Entity = TypeVar("Entity")


class AbstractRepository(ABC):

    def __init__(self):
        self.seen: set[Entity] = set()

    def add(self, entity: Entity) -> UUID:
        id_ = self._add(entity)
        self.seen.add(entity)
        return id_

    def get(self, id_: UUID) -> Entity:
        entity = self._get(id_)
        if entity:
            self.seen.add(entity)
        return entity

    def delete(self, id_: UUID):
        entity = self._delete(id_)
        if entity:
            self.seen.add(entity)

    def update(self, id_: UUID, attribute: str, new_value: Any):
        entity = self._update(id_, attribute, new_value)
        if entity:
            self.seen.add(entity)

    @abstractmethod
    def _add(self, entity: Entity) -> None:
        ...

    @abstractmethod
    def _get(self, id_: UUID) -> Entity:
        ...

    @abstractmethod
    def _delete(self, id_: UUID) -> None:
        ...

    @abstractmethod
    def _update(self, id_: UUID, attribute: str, new_value: Any) -> Entity:
        ...


class SQLAlchemyAccountRepository(AbstractRepository):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def _add(self, account: Account) -> UUID:
        self.session.add(account)
        return account.id_

    def _get(self, id_: UUID) -> Account | None:
        stmt = (select(Account)
                .options(joinedload(Account.assets), joinedload(Account.liabilities))
                .filter_by(id_=id_))
        return self.session.execute(stmt).scalars().first()

    def _delete(self, id_: UUID) -> None:
        stmt = (delete(Account)
                .where(Account.id_ == id_)
                .execution_options(synchronize_session="fetch"))
        self.session.execute(stmt)

    def _update(self, id_: UUID, attribute: str, new_value: Any) -> Account:
        account = self._get(id_)
        setattr(account, attribute, new_value)
        return account


class SQLAlchemyOrderRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, order: OrderBase) -> None:
        self.session.add(order)
        return order.id_

    def _get(self, id_: UUID) -> OrderBase | None:
        stmt = (select(OrderBase)
                .filter_by(id_=id_))
        return self.session.execute(stmt).scalars().first()

    def _delete(self, id_: UUID) -> None:
        order = self._get(id_)
        self.session.delete(order)

    def _update(self, id_: UUID, attribute: str, new_value: Any) -> OrderBase:
        order: OrderBase = self._get(id_)
        setattr(order, attribute, new_value)
        return order
