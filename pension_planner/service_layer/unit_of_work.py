from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from pension_planner import config
from pension_planner.adapters.repositories import SQLAlchemyAccountRepository, AbstractRepository, \
    SQLAlchemyOrderRepository


class AbstractUnitOfWork(ABC):
    _repos: dict[str, AbstractRepository] = {}

    def __enter__(self):
        self.init_repositories()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        ...

    def collect_new_events(self):
        for repo in self._repos.values():
            for entity in repo.seen:
                while entity.events:
                    yield entity.events.pop(0)

    @property
    def accounts(self):
        return self._repos["accounts"]

    @property
    def orders(self):
        return self._repos["orders"]

    @abstractmethod
    def init_repositories(self) -> None:
        ...

    @abstractmethod
    def rollback(self):
        ...


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(config.get_sqlite_uri()),
    future=True,
    expire_on_commit=False
)


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        super().__init__()
        self.session_factory = session_factory

    def init_repositories(self) -> None:
        self._repos["accounts"] = SQLAlchemyAccountRepository(self.session)
        self._repos["orders"] = SQLAlchemyOrderRepository(self.session)

    def __enter__(self):
        self.session: Session = self.session_factory()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
