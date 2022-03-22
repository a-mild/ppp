from datetime import date
from uuid import uuid4

import pandas as pd
import pytest

from pension_planner.domain.bank_statement_service import produce_bankstatement, create_series, concat_series, merge
from pension_planner.domain.orders import SingleOrder, StandingOrder


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
    empty = pd.DataFrame()
    merged = concat_series(empty, single_order_series)
    assert len(merged) == 1
    assert merged.index.freq == "MS"


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


def test_merge_one_order(single_order_factory):
    single_order = single_order_factory(
        date_=date(2019, 1, 1),
        amount=1000
    )
    merged = merge(map(create_series, [single_order]))
    assert len(merged) == 1


def test_merge(single_order_factory, standing_order_factory):
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

    bank_statement = produce_bankstatement(account)
    assert len(bank_statement) == 25
    assert bank_statement.loc[max(bank_statement.index), "total"] == 0


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

    bank_statement = produce_bankstatement(account)
    assert bank_statement.loc[max(bank_statement.index), "total"] > 0
