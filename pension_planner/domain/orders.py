from abc import ABC, abstractmethod
from collections.abc import Mapping
from enum import Enum, auto
from typing import Type
from uuid import uuid4, UUID
from datetime import date, datetime
from dataclasses import dataclass, field

from dateutil.rrule import rrule, MONTHLY


# registry for the different payment classes
ORDER_TYPES: dict[str, Type["OrderBase"]] = {}


@dataclass
class OrderBase(ABC):
    name: str
    target_acc_id: UUID
    from_acc_id: UUID | None
    id_: UUID = field(default_factory=uuid4, init=False)

    def __init_subclass__(cls, **kwargs) -> None:
        name = cls.__name__
        ORDER_TYPES[name] = cls

    def __hash__(self):
        return hash(self.id_)

# eq=False lets the subclasses inherit the __hash__ function of the superclass

@dataclass(eq=False)
class SingleOrder(OrderBase):
    date: date
    amount: float

    def get_timeseries(self):
        return {self.date: self.amount}


@dataclass(eq=False)
class StandingOrder(OrderBase):
    start_date: date
    end_date: date
    amount: float

    def get_timeseries(self) -> Mapping[datetime, float]:
        return {ts: self.amount for ts in rrule(MONTHLY, dtstart=self.start_date, until=self.end_date)}


def order_factory(order_type: str, **order_kwargs) -> OrderBase:
    cls = ORDER_TYPES[order_type]
    return cls(**order_kwargs)
