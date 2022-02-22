from uuid import UUID

import pytest

from pension_planner.domain.bank_account import BankAccount
from pension_planner.repository.bank_account_repo import AbstractBankAccountRepository
from pension_planner.service_layer import messagebus
from pension_planner.service_layer.events import BankAccountCreated
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class FakeBankAccountRepository(AbstractBankAccountRepository):

    def __init__(self):
        super().__init__()
        self.data: dict[UUID, BankAccount] = {}

    def _add(self, bank_account: BankAccount) -> None:
        id_ = bank_account.id_
        self.data[id_] = bank_account

    def _get(self, id_: UUID) -> BankAccount:
        return self.data[id_]

    def _delete(self, id_: UUID) -> BankAccount:
        return self.data.pop(id_)


class FakeUnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.accounts = FakeBankAccountRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


def test_add_bank_account():
    uow = FakeUnitOfWork()
    event = BankAccountCreated(name="test")
    results = messagebus.handle(event, uow=uow)
    assert results == ["test"]