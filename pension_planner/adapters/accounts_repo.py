from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from pension_planner.domain.account import Account

import sqlalchemy


class AbstractAccountRepository(ABC):

    def __init__(self):
        self.seen: set[Account] = set()

    def add(self, account: Account) -> None:
        self._add(account)
        self.seen.add(account)

    def get(self, id_: UUID) -> Account:
        account = self._get(id_)
        if account:
            self.seen.add(account)
        return account

    @abstractmethod
    def _add(self, account: Account) -> None:
        ...

    @abstractmethod
    def _get(self, id_: UUID) -> Account:
        ...


class SQLAlchemyAccountRepository(AbstractAccountRepository):

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _add(self, account: Account) -> None:
        self.session.add(account)

    def _get(self, id_: UUID) -> Account:
        stmt = select(Account).filter_by(id_=id_)
        return self.session.execute(stmt).scalars().first()
