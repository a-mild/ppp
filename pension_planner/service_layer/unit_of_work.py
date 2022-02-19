from abc import ABC, abstractmethod, ABCMeta
from copy import copy

from pension_planner.adapters.payments_repo import InMemoryPaymentsRepo, AbstractPaymentsRepo
from pension_planner.adapters.bank_statement import PandasBankStatement, AbstractBankStatementRepository


class AbstractUnitOfWork(ABC):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class AbstractPaymentsUnitOfWork(AbstractUnitOfWork, metaclass=ABCMeta):
    payments: AbstractPaymentsRepo


class AbstractBankStatementUnitOfWork(AbstractUnitOfWork, metaclass=ABCMeta):
    bank_statement: AbstractBankStatementRepository


class InMemoryPaymentsUnitOfWork(AbstractPaymentsUnitOfWork):
    payments = InMemoryPaymentsRepo()

    def __init__(self):
        self.data_copy = copy(self.payments.data)

    def commit(self):
        return

    def rollback(self):
        self.payments.data = self.data_copy


class PandasUnitOfWork(AbstractBankStatementUnitOfWork):
    bank_statement = PandasBankStatement()

    def __init__(self):
        # save df for rollback
        self.df_copy = self.bank_statement.df.copy(deep=True)

    def commit(self):
        # update the sum column
        self.bank_statement._update_total()

    def rollback(self):
        self.bank_statement.df = self.df_copy
