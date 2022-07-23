from datetime import date

import pandas as pd

from pension_planner.domain.bank_statement_service import create_series, concat_series, merge, \
    BankStatement


def test_create_series(single_order_factory, standing_order_factory):
    single_order = single_order_factory(
        date_=date(2019, 1, 1),
        amount=1000
    )
    standing_order = standing_order_factory(
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100
    )
    single_order_series = create_series(single_order)
    standing_order_series = create_series(standing_order)
    assert single_order_series.tolist() == [1000]
    assert standing_order_series.tolist() == [i * 100 for i in range(1, 13)]


def test_concat_series_with_empty_df(single_order_factory):
    single_order = single_order_factory(
        date_=date(2019, 1, 1),
        amount=1000
    )
    single_order_series = create_series(single_order)
    empty = pd.DataFrame(index=pd.DatetimeIndex([]))
    concatenated = concat_series(empty, single_order_series)
    assert len(concatenated) == 1
    assert concatenated.index.freq == "MS"
    assert concatenated.index.is_monotonic is True


def test_concat_two_series(single_order_factory, standing_order_factory):
    single_order = single_order_factory(
        date_=date(2019, 1, 1),
        amount=1000
    )
    standing_order = standing_order_factory(
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100
    )
    single_order_series = create_series(single_order)
    standing_order_series = create_series(standing_order)

    merged = concat_series(single_order_series, standing_order_series)
    assert len(merged) == 24


def test_merge_empty_list():
    result = merge([])
    assert result.empty is True


def test_merge_two_empty_dataframes():
    df1 = pd.DataFrame(index=pd.DatetimeIndex([]))
    df2 = pd.DataFrame(index=pd.DatetimeIndex([]))
    result = merge([df1, df2])
    assert result.empty is True


def test_merge_one_order(single_order_factory):
    single_order = single_order_factory(
        date_=date(2019, 1, 1),
        amount=1000
    )
    merged = merge(map(create_series, [single_order]))
    assert len(merged) == 1


def test_merge_two_orders(single_order_factory, standing_order_factory):
    single_order = single_order_factory(
        date_=date(2019, 1, 1),
        amount=1000
    )
    standing_order_1 = standing_order_factory(
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100
    )
    standing_order_2 = standing_order_factory(
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 1),
        amount=200
    )
    single_order_series = create_series(single_order)
    standing_order_1_series = create_series(standing_order_1)
    standing_order_2_series = create_series(standing_order_2)
    series_list = [single_order_series, standing_order_1_series, standing_order_2_series]
    merged = merge(series_list)
    assert len(merged) == 36


def test_bankstatement_for_account_with_no_orders(account_factory):
    account = account_factory()
    bank_statement = BankStatement(account)
    assert bank_statement.all_timeseries.empty is True
    assert bank_statement.total.empty is True
    assert bank_statement.total.name == account.name


def test_bankstatement(account_factory, single_order_factory, standing_order_factory):
    single_order = single_order_factory(
        date_=date(2021, 12, 1),
        amount=2400
    )
    standing_order_1 = standing_order_factory(
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100
    )
    standing_order_2 = standing_order_factory(
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 1),
        amount=100
    )
    account = account_factory(
        interest_rate=0.0,
        assets=[standing_order_1, standing_order_2],
        liabilities=[single_order],
    )

    bank_statement = BankStatement(account)
    assert len(bank_statement.all_timeseries) == 24
    total = bank_statement.total
    assert total.name == account.name
    assert len(total) == 25
    assert total.iloc[-1] == 0


def test_bankstatement_with_interest_rate(
        account_factory, single_order_factory, standing_order_factory):
    single_order = single_order_factory(
        date_=date(2021, 12, 1),
        amount=2400
    )
    standing_order_1 = standing_order_factory(
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100
    )
    standing_order_2 = standing_order_factory(
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 1),
        amount=100
    )
    account = account_factory(
        interest_rate=0.1,
        assets=[standing_order_1, standing_order_2],
        liabilities=[single_order],
    )

    bank_statement = BankStatement(account)
    assert bank_statement.total.iloc[-1] > 0


def test_merge_totals_of_empty_bankstatements(account_factory):
    account1 = account_factory()
    account2 = account_factory()
    bstmt1 = BankStatement(account1)
    bstmt2 = BankStatement(account2)

    totals = merge([bstmt.total for bstmt in [bstmt1, bstmt2]])
    assert account1.name in totals.columns
    assert account2.name in totals.columns
    assert totals.empty is True


def test_merge_totals_of_bankstatements(
        account_factory, single_order_factory, standing_order_factory):
    single_order = single_order_factory(
        date_=date(2021, 12, 1),
        amount=2400
    )
    standing_order_1 = standing_order_factory(
        start_date=date(2020, 1, 1),
        end_date=date(2020, 12, 1),
        amount=100
    )
    standing_order_2 = standing_order_factory(
        start_date=date(2021, 1, 1),
        end_date=date(2021, 12, 1),
        amount=100
    )
    account1 = account_factory(
        interest_rate=0.0,
        assets=[standing_order_1, standing_order_2],
        liabilities=[],
    )
    account2 = account_factory(
        interest_rate=0.0,
        assets=[],
        liabilities=[single_order]
    )

    bank_statement1 = BankStatement(account1)
    bank_statement2 = BankStatement(account2)

    totals = merge([bstmt.total for bstmt in [bank_statement1, bank_statement2]])
    assert account1.name in totals.columns
    assert account2.name in totals.columns
    assert totals.empty is False
    assert len(totals) == 25        # not 24 because we had to add a row
