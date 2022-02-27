import pytest

from pension_planner.domain.account import Account
from pension_planner.repository.account_repo import InMemoryAccountRepository

@pytest.fixture
def bank_account_repo():
    return InMemoryAccountRepository()


@pytest.fixture
def bank_account():
    return Account()


def test_add_bank_account(bank_account_repo, bank_account):
    id_ = bank_account_repo.add(bank_account)
    assert (id_ in bank_account_repo.data) is True

def test_get_bank_account(bank_account_repo, bank_account):
    id_ = bank_account.id_
    bank_account_repo.data = {id_: bank_account}
    revived = bank_account_repo.get(id_)
    assert revived == bank_account

def test_delete_bank_account(bank_account_repo, bank_account):
    id_ = bank_account.id_
    bank_account_repo.data = {id_: bank_account}
    deleted = bank_account_repo.delete(id_)
    assert deleted == bank_account
