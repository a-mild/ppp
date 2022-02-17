from uuid import uuid4

import pandas as pd
import pytest

from pension_planner.adapters.bank_statement import PandasBankStatement


class TestPandasBankStatement:

    @pytest.fixture
    def repo(self) -> PandasBankStatement:
        return PandasBankStatement()

    def test_upsert_payment(self, constant_payment, repo):
        ts = constant_payment.get_timeseries()
        id_ = constant_payment.id_
        repo.upsert_payment(id_, ts)
        assert id_ in repo.df.columns
        assert repo.df[id_].to_dict() == ts

    def test_delete_payment(self, repo):
        id_ = uuid4()
        repo.df[id_] = pd.Series([100] * 10)
        repo.delete_payment(id_)
        assert (id_ in repo.df.columns) is False

    def test_fetch_payment_timeseries(self, repo):
        id_ = uuid4()
        ts = [100] * 10
        repo.df[id_] = pd.Series(ts)
        assert repo.fetch_payment_timeseries(id_) == ts

    def test_fetch_total_payment_timeseries(self, repo):
        pass
