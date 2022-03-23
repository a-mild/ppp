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
    return functools.reduce(concat_series, series_list, pd.DataFrame(index=pd.DatetimeIndex([])))


def step(balance, payment, interest_rate):
    return balance*(1 + interest_rate) + payment


def calc_interest(series: pd.Series, interest_rate: float = 0.0) -> pd.Series:
    # convert interest_rate to rate per month
    interest_rate_per_month = (1 + interest_rate)**(1/12) - 1
    return list(itertools.accumulate(series, lambda a, b: step(a, b, interest_rate_per_month)))


class BankStatement:

    def __init__(self, account: Account):
        self.account = account

    @property
    def assets(self) -> pd.DataFrame:
        return merge(list(map(create_series, self.account.assets)))

    @property
    def liabilities(self) -> pd.DataFrame:
        return -merge(list(map(create_series, self.account.liabilities)))  # mind the minus!

    @property
    def all_timeseries(self):
        return merge([self.assets, self.liabilities])

    @property
    def total(self):
        all_ts = self.all_timeseries
        if all_ts.empty is True:
            return pd.Series(index=pd.DatetimeIndex([]), name=self.account.name)
        all_ts.loc[min(all_ts.index) - 1 * all_ts.index.freq] = 0
        all_ts = all_ts.sort_index()
        payments = (all_ts
                    .diff(1)
                    # .dropna(axis="rows")
                    .sum(axis=1)
                    )
        data = calc_interest(payments, self.account.interest_rate)
        return pd.Series(data, index=payments.index, name=self.account.name)
