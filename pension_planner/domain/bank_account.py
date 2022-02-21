from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from pension_planner.domain.orders import OrderBase


def name_generator():
    counter = 0
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
