from datetime import date

import pytest

from pension_planner.domain.orders import SingleOrder, BalanceSheetSide, StandingOrder


@pytest.fixture
def single_payment() -> SingleOrder:
    name = "single payment"
    side = BalanceSheetSide.asset
    ts = date(2022, 12, 1)
    amount = 100.00
    return SingleOrder(name=name, side=side, timestamp=ts, amount=amount)



@pytest.fixture
def constant_payment() -> StandingOrder:
    name = "constant payment"
    side = BalanceSheetSide.asset
    from_ts = date(2021, 1, 1)
    until_ts = date(2022, 1, 1)
    amount = 100
    return StandingOrder(name=name, side=side, from_ts=from_ts, until_ts=until_ts, amount=amount)
