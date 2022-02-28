from uuid import UUID

from pension_planner.adapters.accounts_repo import AbstractAccountRepository
from pension_planner.domain.account import Account
from pension_planner.service_layer import messagebus
from pension_planner.domain.commands import OpenAccount
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


class FakeBankAccountRepository(AbstractAccountRepository):

    def __init__(self):
        super().__init__()
        self.data: dict[UUID, Account] = {}

    def _add(self, account: Account) -> None:
        id_ = account.id_
        self.data[id_] = account

    def _get(self, id_: UUID) -> Account:
        return self.data[id_]


class FakeAccountsUnitOfWork(AbstractUnitOfWork):

    def __init__(self):
        self.accounts = FakeBankAccountRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass

    def collect_new_events(self):
        for account in self.accounts.seen:
            while account.events:
                yield account.events.pop(0)


def test_open_bank_account():
    uow = FakeAccountsUnitOfWork()
    command = OpenAccount()
    [account] = messagebus.handle(command, uow=uow)
    assert uow.committed is True
    assert account.name == command.name
    assert account.assets == command.assets
    assert account.liabilities == command.liabilities
    assert account.interest_rate == command.interest_rate
