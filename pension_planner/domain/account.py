from dataclasses import dataclass, field
from uuid import UUID, uuid4

from pension_planner.domain import events
from pension_planner.domain.orders import OrderBase
from pension_planner.domain.commands import Command


@dataclass
class Account:
    name: str
    interest_rate: float
    assets: list[OrderBase] = field(default_factory=list)
    liabilities: list[OrderBase] = field(default_factory=list)
    id_: UUID = field(default_factory=uuid4)
    events: list[Command] = field(default_factory=list, init=False, compare=False)

    def __post_init__(self):
        self._initialized = True
        event = events.AccountOpened(id_=self.id_)
        self.events.append(event)

    def __hash__(self):
        return hash(self.id_)

    def __setattr__(self, key, value):
        if getattr(self, "_initialized", False) is True:
            old_value = getattr(self, key)
            if old_value == value:
                return
            event = events.AccountAttributeUpdated(
                id_=self.id_,
                attribute=key,
                old_value=old_value,
                new_value=value
            )
            self.events.append(event)
        super().__setattr__(key, value)
