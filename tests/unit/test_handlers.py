from uuid import UUID

from pension_planner.domain.account import Account
from pension_planner.repository.account_repo import AbstractBankAccountRepository
from pension_planner.service_layer import messagebus
from pension_planner.domain.commands import OpenAccount
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class FakeBankAccountRepository(AbstractBankAccountRepository):

    def __init__(self):
        super().__init__()
        self.data: dict[UUID, Account] = {}

    def _add(self, bank_account: Account) -> None:
        id_ = bank_account.id_
        self.data[id_] = bank_account

    def _get(self, id_: UUID) -> Account:
        return self.data[id_]

    def _delete(self, id_: UUID) -> Account:
        return self.data.pop(id_)


class FakeUnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.accounts = FakeBankAccountRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


def test_open_bank_account():
    uow = FakeUnitOfWork()
    command = OpenAccount(name="test")
    [account] = messagebus.handle(command, uow=uow)
    assert account.name == command.name
    assert account.orders == command.orders
    assert account.interest_rate == command.interest_rate