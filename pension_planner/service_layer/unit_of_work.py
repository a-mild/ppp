from abc import ABC, abstractmethod
from copy import copy

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


class InMemoryBankAccountRepositoryUnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.accounts: InMemoryAccountRepository = InMemoryAccountRepository()
        self.data_copy = copy(self.accounts.data)

    def commit(self):
        pass

    def rollback(self):
        self.accounts.data = self.data_copy
