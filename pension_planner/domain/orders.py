from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import Enum, auto
from uuid import uuid4, UUID
from datetime import date, datetime
from dataclasses import dataclass, field

from dateutil.rrule import rrule, MONTHLY


class BalanceSheetSide(Enum):
    asset = auto()
    liability = auto()


# registry for the different payment classes
ORDER_TYPES: dict[str, "OrderBase"] = {}


@dataclass
class OrderBase(ABC):
    name: str
    side: BalanceSheetSide
    id_: UUID = field(default_factory=uuid4, init=False)

    def __init_subclass__(cls, **kwargs) -> None:
        name = cls.__name__
        ORDER_TYPES[name] = cls

    @abstractmethod
    def get_timeseries(self) -> Mapping[date, float]:
        ...


@dataclass
class SingleOrder(OrderBase):
    timestamp: date
    amount: float

    def get_timeseries(self):
        return {self.timestamp: self.amount}


@dataclass
class StandingOrder(OrderBase):
    from_ts: date
    until_ts: date
    amount: float

    def get_timeseries(self) -> Mapping[datetime, float]:
        return {ts: self.amount for ts in rrule(MONTHLY, dtstart=self.from_ts, until=self.until_ts)}


def payment_factory(payment_type: str, **payment_kwargs) -> OrderBase:
    cls = PAYMENT_TYPES[payment_type]
    return cls(**payment_kwargs)
