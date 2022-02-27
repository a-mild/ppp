from pension_planner.adapters.accounts_repo import SQLAlchemyAccountRepository


def test_add_account(session, account):
    repo = SQLAlchemyAccountRepository(session)
    repo.add(account)
    assert repo.get(account.id_) == account
