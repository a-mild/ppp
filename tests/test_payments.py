from datetime import date, datetime

from dateutil.relativedelta import relativedelta


def test_single_payment_timeseries(single_order) -> None:
    payment = single_order
    timeseries = payment.get_timeseries()
    assert timeseries == {date(2022, 12, 1): 100.00}


def test_constant_payment_timeseries(standing_order) -> None:
    payment = standing_order
    timeseries = payment.get_timeseries()
    assert len(timeseries) == 13
    start_date = datetime(2021, 1, 1)
    for i, ts in enumerate(sorted(timeseries.keys())):
        assert ts == start_date + i*relativedelta(months=1)
