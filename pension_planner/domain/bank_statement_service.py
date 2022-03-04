from abc import ABC, abstractmethod
from datetime import date
from typing import Any
from uuid import UUID

import pandas as pd
from dateutil.rrule import rrule, MONTHLY

from pension_planner.domain.account import Account
from pension_planner.domain.orders import OrderBase, SingleOrder, StandingOrder


def build_timeseries(order: OrderBase):
    if isinstance(order, SingleOrder):
        dtstart = order.date
        until = order.date
    elif isinstance(order, StandingOrder):
        dtstart = order.start_date
        until = order.end_date
    return {ts: i*order.amount
            for i, ts in enumerate(rrule(MONTHLY, dtstart=dtstart, until=until), start=1)}


def calc_interest(series: pd.Series, interest_rate: float = 0.0) -> pd.Series:
    for i in range(1, len(series)):
        series.iloc[i] = series.iloc[i] + series.iloc[i-1]*interest_rate*int(series.iloc[i] >= 0)
    return series


class AccountRepo:

    def __init__(self, interest_rate: float = 0.0) -> None:
        self.interest_rate = interest_rate
        self.df: pd.DataFrame = pd.DataFrame()
        self.total: pd.DataFrame = pd.DataFrame()

    def add_series(self, series: pd.Series):
        self.df = self.df.join(series, how="outer").asfreq("MS").fillna(method="ffill").fillna(0)
        self.total = (self.df.sum(axis=1)
                      .pipe(lambda x: calc_interest(x, self.interest_rate)))

    def delete_series(self, order_id: UUID):
        self.df = self.df.drop(columns=order_id)
        self.total = (self.df.sum(axis=1)
                      .pipe(lambda x: calc_interest(x, self.interest_rate)))

    def update_series(self, series: pd.Series):
        self.df = self.df.drop(columns=series.name)


class AbstractBankStatementRepository(ABC):

    @abstractmethod
    def add_account(self, account: Account):
        ...

    @abstractmethod
    def delete_account(self, id_: UUID):
        ...

    @abstractmethod
    def update_interest_rate(self, id_: UUID):
        ...

    @abstractmethod
    def add_order(self, order: OrderBase):
        ...

    @abstractmethod
    def delete_order(self, id_: UUID):
        ...

    @abstractmethod
    def update_order(self, id_: UUID, attribute: str, new_value: Any):
        ...

    @abstractmethod
    def get_total(self):
        ...


class PandasBankStatementRepository(AbstractBankStatementRepository):

    accounts: dict[UUID, AccountRepo] = {}

    def add_account(self, account: Account):
        self.accounts[account.id_] = AccountRepo(account.interest_rate)

    def delete_account(self, id_: UUID):
        self.accounts.pop(id_)

    def update_interest_rate(self, id_: UUID, interest_rate: float):
        self.accounts[id_].interest_rate = interest_rate

    def add_order(self, order: OrderBase):
        ts = build_timeseries(order)
        series = pd.Series(ts, name=order.id_)
        if order.from_acc_id is not None:
            self.accounts[order.from_acc_id].add_series(-series)
        if order.target_acc_id is not None:
            self.accounts[order.target_acc_id].add_series(series)

    def delete_order(self, id_: UUID):
        for acc_id, acc_repo in self.accounts.items():
            if id_ in acc_repo.df.columns:
                acc_repo.delete_series(id_)

    def update_order(self, order: OrderBase):
        # workaround: remove from all first then add new series
        self.delete_order(order.id_)
        self.add_order(order)


    def get_total(self) -> pd.Series:
        total = (pd.DataFrame()
                 .join([acc_repo.total for acc_repo in self.accounts.values()], how="outer")
                 .fillna(method="ffill")
                 .fillna(0)
                 .sum(axis=1))
        return total

    @classmethod
    def reset(cls):
        cls.orders = {}


if __name__ == "__main__":
    single = SingleOrder(name="single", from_acc=0, target_acc=1, date=date(2020, 1, 1), amount=100)
    ts_single = build_timeseries(single)