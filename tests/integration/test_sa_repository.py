from datetime import date
from uuid import uuid4

import pytest
from src.pension_planner.domain import AccountOpened, AccountAttributeUpdated
from src.pension_planner.domain import SingleOrder


pytestmark = pytest.mark.usefixtures("mappers")


def test_sa_repo_can_add_account(sa_account_repo, account_factory):
    acc = account_factory()
    acc_id = sa_account_repo.add(acc)
    sa_account_repo.session.commit()
    revived = sa_account_repo.get(acc_id)
    assert revived == acc
    assert revived.events == [AccountOpened(id_=acc_id)]


def test_sa_repo_can_list_accounts(
        sa_account_repo, sa_order_repo, account_factory, single_order_factory, standing_order_factory):
    acc1 = account_factory()
    acc2 = account_factory()
    acc1_id = sa_account_repo.add(acc1)
    acc2_id = sa_account_repo.add(acc2)
    sa_account_repo.session.commit()
    single_order = single_order_factory(
        date_=date(2020, 1, 1),
        target_acc_id=acc1_id,
        amount=1000.0,
    )
    standing_order = standing_order_factory(
        target_acc_id=acc2_id,
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100.0
    )
    sa_order_repo.add(single_order)
    sa_order_repo.add(standing_order)
    sa_order_repo.session.commit()

    accounts = sa_account_repo.list()
    assert len(accounts) == 2
    assert acc1 in accounts
    assert acc2 in accounts


def test_sa_repo_returns_none_for_nonexistent_account(sa_account_repo, account_factory):
    acc = account_factory()
    sa_account_repo.add(acc)
    sa_account_repo.session.commit()
    random_id = uuid4()
    result = sa_account_repo.get(random_id)
    assert result is None


def test_rollback_does_not_add(sa_account_repo, account_factory):
    acc = account_factory()
    acc_id = sa_account_repo.add(acc)
    sa_account_repo.session.rollback()
    result = sa_account_repo.get(acc_id)
    assert result is None


def test_sa_repo_can_delete_account(sa_account_repo, account_factory):
    account = account_factory()
    acc_id = sa_account_repo.add(account)
    sa_account_repo.delete(acc_id)
    assert sa_account_repo.get(acc_id) is None


def test_sa_repo_can_update_account(sa_account_repo, account_factory):
    account = account_factory()
    old_name = account.name
    old_interest_rate = account.interest_rate
    acc_id = sa_account_repo.add(account)
    sa_account_repo.session.commit()
    sa_account_repo.update(acc_id, "name", "Girokonto #42")
    sa_account_repo.update(acc_id, "interest_rate", 0.001)
    sa_account_repo.session.commit()
    revived = sa_account_repo.get(acc_id)
    assert revived.name == "Girokonto #42"
    assert revived.interest_rate == 0.001
    event_name = AccountAttributeUpdated(
        id_=acc_id,
        attribute="name",
        old_value=old_name,
        new_value="Girokonto #42"
    )
    event_interest_rate = AccountAttributeUpdated(
        id_=acc_id,
        attribute="interest_rate",
        old_value=old_interest_rate,
        new_value=0.001
    )
    assert event_name in revived.events
    assert event_interest_rate in revived.events


def test_add_orders(sa_order_repo, single_order_factory, standing_order_factory):
    single_order = single_order_factory()
    standing_order = standing_order_factory()
    single_order_id = sa_order_repo.add(single_order)
    standing_order_id = sa_order_repo.add(standing_order)
    sa_order_repo.session.commit()
    assert sa_order_repo.get(single_order_id) == single_order
    assert sa_order_repo.get(standing_order_id) == standing_order


def test_sa_repo_returns_none_for_nonexistent_order(sa_order_repo, single_order_factory):
    single_order = single_order_factory()
    sa_order_repo.add(single_order)
    sa_order_repo.session.commit()
    random_id = uuid4()
    result = sa_order_repo.get(random_id)
    assert result is None


def test_delete_orders(sa_order_repo, single_order_factory, standing_order_factory):
    single_order = single_order_factory()
    standing_order = standing_order_factory()
    single_order_id = sa_order_repo.add(single_order)
    standing_order_id = sa_order_repo.add(standing_order)
    sa_order_repo.session.commit()

    sa_order_repo.delete(single_order_id)
    sa_order_repo.delete(standing_order_id)
    sa_order_repo.session.commit()

    assert sa_order_repo.get(single_order_id) is None
    assert sa_order_repo.get(standing_order_id) is None


def test_update_order(sa_account_repo, sa_order_repo, single_order_factory, account_factory):
    account = account_factory()
    sa_account_repo.add(account)
    sa_account_repo.session.commit()
    single_order = single_order_factory()
    single_order_id = sa_order_repo.add(single_order)
    sa_order_repo.session.commit()
    sa_order_repo.update(single_order_id, "name", "Riesiger Auftrag")
    sa_order_repo.update(single_order_id, "from_acc_id", account.id_)
    sa_order_repo.update(single_order_id, "date", date(2042, 1, 1))
    sa_order_repo.update(single_order_id, "amount", 1_000_000)
    sa_order_repo.session.commit()
    revived: SingleOrder = sa_order_repo.get(single_order_id)
    assert revived.name == "Riesiger Auftrag"
    assert revived.from_acc_id == account.id_
    assert revived.target_acc_id is None
    assert revived.date == date(2042, 1, 1)
    assert revived.amount == 1_000_000
    assert len(revived.events) == 5


def test_can_backfill_account_assets_and_liabilities_when_adding_an_order(
        sa_account_repo, sa_order_repo, account_factory, single_order_factory
):
    account = account_factory()
    account_id = sa_account_repo.add(account)
    sa_account_repo.session.commit()
    order_1 = single_order_factory(from_acc_id=account_id)
    order_2 = single_order_factory(target_acc_id=account_id)
    order_1_id = sa_order_repo.add(order_1)
    order_2_id = sa_order_repo.add(order_2)
    sa_order_repo.session.commit()
    order_1_revived = sa_order_repo.get(order_1_id)
    order_2_revived = sa_order_repo.get(order_2_id)
    account_revived = sa_account_repo.get(account_id)
    assert order_1_revived in account_revived.liabilities
    assert order_2_revived in account_revived.assets


def test_order_backref_resets_to_none_after_deleting_ref_account(
        sa_account_repo, sa_order_repo, account_factory, single_order_factory
):
    account = account_factory()
    account_id = sa_account_repo.add(account)
    sa_account_repo.session.commit()
    order_1 = single_order_factory(from_acc_id=account_id)
    order_2 = single_order_factory(target_acc_id=account_id)
    order_1_id = sa_order_repo.add(order_1)
    order_2_id = sa_order_repo.add(order_2)
    sa_order_repo.session.commit()
    sa_account_repo.delete(account_id)
    sa_account_repo.session.commit()
    order_1_revived = sa_order_repo.get(order_1_id)
    order_2_revived = sa_order_repo.get(order_2_id)
    assert order_1_revived.from_acc_id is None
    assert order_2_revived.target_acc_id is None


def test_assets_and_liabilities_are_updated_after_order_deletion(
        sa_account_repo, sa_order_repo, account_factory, single_order_factory
):
    account = account_factory()
    account_id = sa_account_repo.add(account)
    sa_account_repo.session.commit()
    order_1 = single_order_factory(from_acc_id=account_id)
    order_2 = single_order_factory(target_acc_id=account_id)
    order_1_id = sa_order_repo.add(order_1)
    order_2_id = sa_order_repo.add(order_2)
    sa_order_repo.session.commit()

    sa_order_repo.delete(order_1_id)
    sa_order_repo.session.commit()

    account_revived = sa_account_repo.get(account_id)
    assert account_revived.liabilities == []
    assert account_revived.assets == [order_2]
    sa_order_repo.delete(order_2_id)
    sa_order_repo.session.commit()
    account_revived = sa_account_repo.get(account_id)
    assert account_revived.liabilities == []
    assert account_revived.assets == []
