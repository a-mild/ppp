import itertools
from datetime import date
from uuid import uuid4

import pandas as pd
import pytest
from dateutil.rrule import rrule, MONTHLY

from pension_planner.adapters.bank_statement import PandasBankStatement


def make_timeseries(amount, from_ts, until_ts):
    return {ts: amount for ts in rrule(MONTHLY, dtstart=from_ts, until=until_ts)}


@pytest.fixture
def ts_2019():
    return make_timeseries(100, date(2019, 1, 1), date(2019, 12, 1))


@pytest.fixture
def ts_2021():
    return make_timeseries(100, date(2021, 1, 1), date(2021, 12, 1))


class TestPandasBankStatement:

    @pytest.fixture
    def repo(self) -> PandasBankStatement:
        return PandasBankStatement()

    def test_upsert_payment(self, repo, ts_2019):
        id_ = uuid4()
        repo.upsert_payment(id_, ts_2019)
        assert id_ in repo.df.columns
        assert repo.df[id_]["values"].to_dict() == ts_2019
        cumsum_expected = list(itertools.accumulate(ts_2019.values()))
        assert repo.df[id_]["cumsum"].to_list() == cumsum_expected

    def test_upsert_two_payments(self, repo, ts_2019, ts_2021):
        id1 = uuid4()
        id2 = uuid4()
        repo.upsert_payment(id1, ts_2019)
        repo.upsert_payment(id2, ts_2021)
        assert len(repo.df) == 36
        from_, to = date(2020, 1, 1), date(2021, 12, 1)
        assert (repo.df[id1]["values"].loc[from_:to] == 0).all() == True
        last = repo.df[id1]["cumsum"].iloc[11]
        assert (repo.df[id1]["cumsum"].loc[from_:to] == last).all() == True
        # id2
        from_, to = date(2019, 1, 1), date(2020, 12, 1)
        assert (repo.df[id2]["values"].loc[from_:to] == 0).all() == True
        assert (repo.df[id2]["cumsum"].loc[from_:to] == 0).all() == True

    def test_delete_payment(self, repo):
        id_ = uuid4()
        repo.df[id_] = pd.Series([100] * 10)
        repo.delete_payment(id_)
        assert (id_ in repo.df.columns) is False

    @pytest.mark.skip(reason="Not sure what i want from this function yet")
    def test_fetch_payment_timeseries(self, repo):
        id_ = uuid4()
        ts = [100] * 10
        repo.df[id_]["values"] = pd.Series(ts)
        assert repo.fetch_payment_timeseries(id_) == ts

    def test_fetch_total_payment_timeseries(self, repo, ts_2019, ts_2021):
        id1 = uuid4()
        id2 = uuid4()
        repo.upsert_payment(id1, ts_2019)
        repo.upsert_payment(id2, ts_2021)
        repo._update_total()
        totals = repo.fetch_total_timeseries()
        expected = [100.0*i for i in range(1, 13)] + 12 * [1200.0] + [1200+100.0*i for i in range(1, 13)]
        assert list(totals.values()) == expected
