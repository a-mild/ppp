from datetime import date
from uuid import uuid4

import pytest

from pension_planner.domain.bank_statement_service import PandasBankStatementRepository
from pension_planner.domain.orders import SingleOrder, StandingOrder


@pytest.fixture
def bs_repo():
    repo = PandasBankStatementRepository()
    yield repo
    repo.reset()


def test_can_add_account(bs_repo, base_account):
    bs_repo.add_account(base_account)
    assert base_account.id_ in bs_repo.accounts


def test_can_delete_account(bs_repo, base_account):
    bs_repo.add_account(base_account)
    assert base_account.id_ in bs_repo.accounts
    bs_repo.delete_account(base_account.id_)
    assert base_account.id_ not in bs_repo.accounts


def test_can_change_interest_rate(bs_repo, base_account):
    bs_repo.add_account(base_account)
    bs_repo.update_interest_rate(base_account.id_, 0.10)
    assert bs_repo.accounts[base_account.id_].interest_rate == 0.10


def test_can_add_orders(bs_repo, base_account, single_order, standing_order):
    single = SingleOrder(
        name="1",
        from_acc_id=base_account.id_,
        target_acc_id=None,
        date=date(2020, 1, 1),
        amount=100.0
    )
    standing = StandingOrder(
        name="1",
        from_acc_id=base_account.id_,
        target_acc_id=None,
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100.0
    )
    bs_repo.add_account(base_account)
    bs_repo.add_order(single)
    assert single.id_ in bs_repo.accounts[base_account.id_].df.columns
    assert bs_repo.accounts[base_account.id_].df[single.id_].tolist() == [-single.amount]
    bs_repo.add_order(standing)
    assert standing.id_ in bs_repo.accounts[base_account.id_].df.columns
    expected = [-standing.amount*i for i in range(1, 13)]
    assert bs_repo.accounts[base_account.id_].df[standing.id_].tolist() == expected


def test_can_delete_order(bs_repo, base_account, single_order):
    bs_repo.add_account(base_account)
    bs_repo.add_order(single_order)
    bs_repo.delete_order(single_order.id_)
    assert single_order.id_ not in bs_repo.accounts[base_account.id_].df.columns


def test_can_update_orders(bs_repo, base_account, single_order, standing_order):
    bs_repo.add_account(base_account)
    bs_repo.add_order(single_order)
    bs_repo.add_order(standing_order)

    # turn account to none
    single_order.from_acc_id = None
    bs_repo.update_order(single_order)
    assert single_order.id_ not in bs_repo.accounts[base_account.id_].df.columns
    # move to asset
    single_order.target_acc_id = base_account.id_
    bs_repo.update_order(single_order)
    assert single_order.id_ in bs_repo.accounts[base_account.id_].df.columns
    # change value
    single_order.amount = 2*single_order.amount
    old_series = bs_repo.accounts[base_account.id_].df[single_order.id_]
    bs_repo.update_order(single_order)
    assert (bs_repo.accounts[base_account.id_].df[single_order.id_] == 2*old_series).all() is True


def test_get_total(bs_repo, base_account, single_order, standing_order):
    bs_repo.add_account(base_account)
    bs_repo.add_order(single_order)
    bs_repo.add_order(standing_order)
    assert bs_repo.get_total().to_list()[-1] == 0

