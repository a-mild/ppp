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
    df: pd.DataFrame = make_empty_df()

    @classmethod
    def upsert_payment(cls, id_: UUID, timeseries: Mapping[datetime, float]) -> None:
        other = make_empty_df()
        other[id_, "values"] = pd.Series(timeseries)
        cls.df = pd.concat([cls.df, other], axis=1)
        cls.df[id_, "cumsum"] = cls.df[id_, "values"].cumsum()

    @classmethod
    def delete_payment(cls, id_: UUID) -> None:
        cls.df.drop(columns=[id_], inplace=True)

    @classmethod
    def fetch_payment_timeseries(cls, id_: UUID) -> Iterable[tuple[datetime, float]]:
        return cls.df[id_].to_

    @classmethod
    def fetch_total_timeseries(cls) -> Iterable[tuple[datetime, float]]:
        pass
