from abc import ABC, abstractmethod
from uuid import UUID

from pension_planner.domain.bank_account import BankAccount


class AbstractBankAccountRepository(ABC):

    def __init__(self):
        self.seen: set[BankAccount] = set()

    def add(self, bank_account: BankAccount):
        self._add(bank_account)
        self.seen.add(bank_account)

    def get(self, id_: UUID) -> BankAccount:
        bank_account = self._get(id_)
        if bank_account:
            self.seen.add(bank_account)
        return bank_account

    def delete(self, id_: UUID) -> BankAccount:
        bank_account = self._delete(id_)
        if bank_account:
            self.seen.add(bank_account)
        return bank_account

    @abstractmethod
    def _add(self, bank_account: BankAccount) -> None:
        ...

    @abstractmethod
    def _get(self, id_: UUID) -> BankAccount:
        ...

    @abstractmethod
    def _delete(self, id_: UUID) -> BankAccount:
        ...


class InMemoryBankAccountRepository(AbstractBankAccountRepository):
    data: dict[UUID, BankAccount] = {}

    def _add(self, bank_account: BankAccount) -> BankAccount:
        id_ = bank_account.id_
        self.data[id_] = bank_account
        return bank_account

    def _get(self, id_: UUID) -> BankAccount:
        return self.data[id_]

    def list_all(self) -> list[BankAccount]:
        return [acc for acc in self.data.values()]

    def _delete(self, id_: UUID) -> BankAccount | None:
        return self.data.pop(id_, None)
