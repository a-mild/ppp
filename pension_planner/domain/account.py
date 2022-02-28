from dataclasses import dataclass, field
from uuid import UUID, uuid4

from pension_planner.domain.orders import OrderBase
from pension_planner.domain.commands import Command


@dataclass
class Account:
    name: str
    interest_rate: float
    assets: list[OrderBase] #= field(default_factory=list)
    liabilities: list[OrderBase] #= field(default_factory=list)
    id_: UUID = field(default_factory=uuid4)
    events: list[Command] = field(default_factory=list, init=False)

    def __hash__(self):
        return hash(self.id_)
