from abc import ABC, abstractmethod
from collections.abc import Mapping, Iterable
from datetime import datetime, date
from uuid import UUID

import pandas as pd


class AbstractBankStatementRepository(ABC):

    @abstractmethod
    def upsert_payment(cls, id_: UUID, timeseries: Mapping[date, float]) -> None:
        ...

    @abstractmethod
    def delete_payment(cls, id_: UUID) -> None:
        ...

    @abstractmethod
    def fetch_payment_timeseries(cls, id_: UUID) -> Iterable[tuple[datetime, float]]:
        ...

    @abstractmethod
    def fetch_total_timeseries(cls) -> Iterable[tuple[datetime, float]]:
        ...


def make_empty_df():
    index = pd.DatetimeIndex([])
    mux = pd.MultiIndex(levels=[[], ["values", "cumsum"]],
                        codes=[[], []])
    return pd.DataFrame(index=index, columns=mux)


class PandasBankStatement(AbstractBankStatementRepository):
    df: pd.DataFrame
    total: pd.DataFrame

    def __init__(self):
        PandasBankStatement.df = make_empty_df()
        PandasBankStatement.total = pd.DataFrame(columns=["sums", "cumsums"])

    @classmethod
    def upsert_payment(cls, id_: UUID, timeseries: Mapping[datetime, float]) -> None:
        other = make_empty_df()
        other[id_, "values"] = pd.Series(timeseries)
        merged = pd.concat([cls.df, other]).asfreq("MS")
        merged.loc[:, (slice(None), "values")] = merged.loc[:, (slice(None), "values")].fillna(0)
        for idx, subframe in merged.groupby(merged.columns.get_level_values(0), axis=1):
            merged[idx, "cumsum"] = subframe[idx, "values"].cumsum()
        cls.df = merged

    @classmethod
    def delete_payment(cls, id_: UUID) -> None:
        cls.df.drop(columns=[id_], inplace=True)

    @classmethod
    def fetch_payment_timeseries(cls, id_: UUID) -> Iterable[tuple[datetime, float]]:
        #return cls.df[id_]
        return NotImplementedError

    @classmethod
    def _update_total(cls) -> None:
        res = cls.df.groupby(level=1, axis=1).sum()
        cls.total = res

    @classmethod
    def fetch_total_timeseries(cls) -> Mapping[datetime, float]:
        return cls.total["cumsum"].to_dict()
