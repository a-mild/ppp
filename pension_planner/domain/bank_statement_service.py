import functools
import itertools
from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Union, Iterable
from uuid import UUID

import pandas as pd
from dateutil.rrule import rrule, MONTHLY

from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase, SingleOrder, StandingOrder


def create_series(order: OrderBase):
    ts = order.get_timeseries()
    name = order.name
    return pd.Series(data=ts, name=name)


def concat_series(df: Union[pd.Series, pd.DataFrame], other: Union[pd.Series, pd.DataFrame]) -> pd.DataFrame:
    result = pd.concat([df, other], axis=1).asfreq("MS").fillna(method="ffill").fillna(0)
    result.index.freq = "MS"
    return result


def merge(series_list: Iterable[pd.Series]) -> pd.DataFrame:
    return functools.reduce(concat_series, series_list, pd.DataFrame())


def step(balance, payment, interest_rate):
    return balance*(1 + interest_rate) + payment


def calc_interest(series: pd.Series, interest_rate: float = 0.0) -> pd.Series:
    # convert interest_rate to rate per month
    interest_rate_per_month = (1 + interest_rate)**(1/12) - 1
    return list(itertools.accumulate(series, lambda a, b: step(a, b, interest_rate_per_month)))


def produce_bankstatement(account: Account) -> pd.DataFrame:
    assets = merge(list(map(create_series, account.assets)))
    liabilities = -merge(map(create_series, account.liabilities))   # mind the minus!
    merged = concat_series(assets, liabilities)
    # add one row below
    merged.loc[min(merged.index) - 1*merged.index.freq] = 0
    merged = merged.sort_index()
    payments = (merged
                .diff(1)
                # .dropna(axis="rows")
                .sum(axis=1)
                )
    merged["total"] = calc_interest(payments, account.interest_rate)
    return merged
