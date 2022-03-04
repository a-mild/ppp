import logging
from abc import ABC
from collections.abc import Mapping
from typing import Type
from uuid import uuid4, UUID
from datetime import date, datetime
from dataclasses import dataclass, field

from dateutil.rrule import rrule, MONTHLY

from pension_planner.domain import events
from pension_planner.domain.events import Event

# registry for the different payment classes
ORDER_TYPES: dict[str, Type["OrderBase"]] = {}

# TODO: maybe some nice __new__ or metaclass solution for injecting __setattr__

@dataclass
class OrderBase(ABC):
    name: str
    from_acc_id: UUID | None
    target_acc_id: UUID
    id_: UUID = field(default_factory=uuid4, init=False)
    events: list[Event] = field(default_factory=list, init=False)


    def __post_init__(self):
        self._initialized = True
        event = events.OrderCreated(id_=self.id_)
        self.events.append(event)

    def __init_subclass__(cls, **kwargs) -> None:
        name = cls.__name__
        ORDER_TYPES[name] = cls

    def __setattr__(self, key, value):
        if self._initialized:
            old_value = getattr(self, key)
            logging.debug(f"{old_value=}")
            event = events.OrderAttributeUpdated(
                order_id=self.id_,
                attribute=key,
                old_value=old_value,
                new_value=value)
            self.events.append(event)
            logging.debug(f"Event appended: {event!r}")
        super().__setattr__(key, value)


    def __hash__(self):
        return hash(self.id_)

# eq=False lets the subclasses inherit the __hash__ function of the superclass

@dataclass(eq=False)
class SingleOrder(OrderBase):
    date: date
    amount: float
    _initialized: bool = field(default=False, repr=False)

@dataclass(eq=False)
class StandingOrder(OrderBase):
    start_date: date
    end_date: date
    amount: float
    _initialized: bool = field(default=False, repr=False)

def order_factory(order_type: str, **order_kwargs) -> OrderBase:
    cls = ORDER_TYPES[order_type]
    return cls(**order_kwargs)


ORDER_ATTRIBUTES = ((SingleOrder.__dataclass_fields__.keys() | StandingOrder.__dataclass_fields__.keys())
                    - set(["id_", "events", "_initialized"]))


if __name__ == "__main__":
    so = SingleOrder(name="1", from_acc_id=0, target_acc_id=1, date=date(2222, 2, 2), amount=100)
