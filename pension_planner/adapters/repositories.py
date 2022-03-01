from abc import ABC, abstractmethod
from typing import TypeVar, Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase

Entity = TypeVar("Entity")


class AbstractRepository(ABC):

    def __init__(self):
        self.seen: set[Entity] = set()

    def add(self, entity: Entity) -> None:
        self._add(entity)
        self.seen.add(entity)

    def get(self, id_: UUID) -> Entity:
        entity = self._get(id_)
        if entity:
            self.seen.add(entity)
        return entity

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
    def _update(self, id_: UUID, attribute: str, new_value: Any) -> Entity:
        ...


class SQLAlchemyAccountRepository(AbstractRepository):

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, account: Account) -> None:
        self.session.add(account)

    def _get(self, id_: UUID) -> Account:
        stmt = (select(Account)
                .options(joinedload(Account.assets), joinedload(Account.liabilities))
                .filter_by(id_=id_))
        return self.session.execute(stmt).scalars().first()

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

    def _get(self, id_: UUID) -> Entity:
        stmt = (select(OrderBase)
                .filter_by(id_=id_))
        return self.session.execute(stmt).scalars().first()

    def _update(self, id_: UUID, attribute: str, new_value: Any) -> OrderBase:
        order = self._get(id_)
        setattr(order, attribute, new_value)
        return order
