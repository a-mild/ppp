from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from pension_planner.domain.orders import OrderBase


class Command:
    pass


@dataclass
class ToggleDrawer(Command):
    pass


def account_name_generator():
    counter = 1
    while True:
        yield f"Bankkonto #{counter}"
        counter += 1


name_factory = account_name_generator()


@dataclass
class OpenAccount(Command):
    name: str = field(default_factory=lambda: next(name_factory))
    interest_rate: float = 0.0
    assets: list[OrderBase] = field(default_factory=list)
    liabilities: list[OrderBase] = field(default_factory=list)


@dataclass
class UpdateAccountAttribute(Command):
    id_: UUID
    attribute: str
    new_value: Any
