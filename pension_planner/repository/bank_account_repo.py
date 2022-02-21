from abc import ABC, abstractmethod
from uuid import UUID

from pension_planner.domain.bank_account import BankAccount


class AbstractBankAccountRepository(ABC):

    @abstractmethod
    def add(self, bank_account: BankAccount) -> None:
        ...

    @abstractmethod
    def get(self, id_: UUID) -> BankAccount:
        ...

    @abstractmethod
    def delete(self, id_: UUID) -> None:
        ...


class InMemoryBankAccountRepository(AbstractBankAccountRepository):
    accounts: dict[UUID, BankAccount] = {}

    def add(self, bank_account: BankAccount) -> None:
        id_ = bank_account.id_
        self.accounts[id_] = bank_account

    def get(self, id_: UUID) -> BankAccount:
        return self.accounts[id_]

    def delete(self, id_: UUID) -> None:
        self.accounts.pop(id_)
