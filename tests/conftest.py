from datetime import date

import pytest

from pension_planner.domain.payments import SinglePayment, BalanceSheetSide, ConstantPayment


@pytest.fixture
def single_payment() -> SinglePayment:
    name = "single payment"
    side = BalanceSheetSide.asset
    ts = date(2022, 12, 1)
    amount = 100.00
    return SinglePayment(name=name, side=side, timestamp=ts, amount=amount)



@pytest.fixture
def constant_payment() -> ConstantPayment:
    name = "constant payment"
    side = BalanceSheetSide.asset
    from_ts = date(2021, 1, 1)
    until_ts = date(2022, 1, 1)
    amount = 100
    return ConstantPayment(name=name, side=side, from_ts=from_ts, until_ts=until_ts, amount=amount)
