from collections import defaultdict
from dataclasses import dataclass
from datetime import date

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
    return {ts: order.amount for ts in rrule(MONTHLY, dtstart=dtstart, until=until)}


def pool_timeseries(all_ts):
    pool = defaultdict(list)
    for ts in all_ts:
        for date, amount in ts.items():
            pool[date].append(amount)
    


def build_bank_statement(assets: list[OrderBase], liabilities: list[OrderBase], interest_rate: float):
    dd_assets = defaultdict(list)



if __name__ == "__main__":
    single = SingleOrder(name="single", from_acc=0, target_acc=1, date=date(2020, 1, 1), amount=100)
    ts_single = build_timeseries(single)