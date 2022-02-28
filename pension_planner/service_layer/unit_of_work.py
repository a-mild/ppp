from abc import ABC, abstractmethod
from copy import copy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from pension_planner import config
from pension_planner.adapters.accounts_repo import SQLAlchemyAccountRepository
from pension_planner.adapters.orders_repo import SQLAlchemyOrdersRepository
from pension_planner.repository.account_repo import AbstractBankAccountRepository, InMemoryAccountRepository


class AbstractUnitOfWork(ABC):
    accounts: AbstractBankAccountRepository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...

    def collect_new_events(self):
        for account in self.accounts.seen:
            while account.events:
                yield account.events.pop(0)


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(config.get_sqlite_uri()),
    future=True,
    expire_on_commit=False
)


class SQLAlchemyAccountsUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.accounts = SQLAlchemyAccountRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SQLAlchemyOrdersUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.orders = SQLAlchemyOrdersRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
