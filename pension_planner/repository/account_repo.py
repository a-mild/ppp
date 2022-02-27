from abc import ABC, abstractmethod
from uuid import UUID

from pension_planner.domain.account import Account


class AbstractBankAccountRepository(ABC):

    def __init__(self):
        self.seen: set[Account] = set()

    def add(self, bank_account: Account):
        self._add(bank_account)
        self.seen.add(bank_account)

    def get(self, id_: UUID) -> Account:
        bank_account = self._get(id_)
        if bank_account:
            self.seen.add(bank_account)
        return bank_account

    def delete(self, id_: UUID) -> Account:
        bank_account = self._delete(id_)
        if bank_account:
            self.seen.add(bank_account)
        return bank_account

    @abstractmethod
    def _add(self, bank_account: Account) -> None:
        ...

    @abstractmethod
    def _get(self, id_: UUID) -> Account:
        ...

    @abstractmethod
    def _delete(self, id_: UUID) -> Account:
        ...


class InMemoryAccountRepository(AbstractBankAccountRepository):
    data: dict[UUID, Account] = {}

    def _add(self, account: Account) -> Account:
        id_ = account.id_
        self.data[id_] = account
        return account

    def _get(self, id_: UUID) -> Account:
        return self.data[id_]

    def list_all(self) -> list[Account]:
        return [acc for acc in self.data.values()]

    def _delete(self, id_: UUID) -> Account | None:
        return self.data.pop(id_, None)
