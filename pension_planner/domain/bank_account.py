from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from pension_planner.domain.orders import OrderBase
from pension_planner.service_layer.events import Event


def name_generator():
    counter = 1
    while True:
        yield f"Bankkonto #{counter}"
        counter += 1


name_factory = name_generator()


@dataclass
class BankAccount:
    name: str = field(default_factory=lambda: next(name_factory))
    orders: list[OrderBase] = field(default_factory=list)
    interest_rate: float = 0.0
    id_: UUID = field(default_factory=uuid4)
    events: list[Event] = field(default_factory=list)

    def __hash__(self):
        return hash(self.id_)


