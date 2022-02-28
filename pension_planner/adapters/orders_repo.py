from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from pension_planner.domain.orders import OrderBase



class AbstractOrdersRepository(ABC):

    def __init__(self):
        self.seen: set[OrderBase] = set()

    def add(self, order: OrderBase) -> None:
        self._add(order)
        self.seen.add(order)

    def get(self, id_: UUID) -> OrderBase:
        order = self._get(id_)
        if order:
            self.seen.add(order)
        return order

    @abstractmethod
    def _add(self, order: OrderBase) -> None:
        ...

    @abstractmethod
    def _get(self, id_: UUID) -> OrderBase:
        ...


class SQLAlchemyOrdersRepository(AbstractOrdersRepository):

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, order: OrderBase) -> None:
        self.session.add(order)

    def _get(self, id_: UUID) -> OrderBase:
        stmt = select(OrderBase).filter_by(id_=id_)
        return self.session.execute(stmt).scalars().first()
