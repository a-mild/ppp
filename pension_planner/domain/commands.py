from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Any
from uuid import UUID

from pension_planner.domain.orders import OrderBase


class Command:
    pass


@dataclass
class ToggleDrawer(Command):
    pass


def name_generator(text: str) -> str:
    counter = 1
    while True:
        yield f"{text} #{counter}"
        counter += 1


account_name_factory = name_generator("Konto")
single_order_name_factory = name_generator("Einzelauftrag")
standing_order_name_factory = name_generator("Dauerauftrag")


@dataclass
class OpenAccount(Command):
    name: str = field(default_factory=lambda: next(account_name_factory))
    interest_rate: float = 0.0
    assets: list[OrderBase] = field(default_factory=list)
    liabilities: list[OrderBase] = field(default_factory=list)


@dataclass
class UpdateAccountAttribute(Command):
    id_: UUID
    attribute: str
    new_value: Any


@dataclass
class CreateSingleOrder(Command):
    name: str = field(default_factory=lambda: next(single_order_name_factory))
    target_acc_id: UUID | None = None
    from_acc_id: UUID | None = None
    date: date = date.today()
    amount: float = 100


@dataclass
class CreateStandingOrder(Command):
    name: str = field(default_factory=lambda: next(standing_order_name_factory))
    target_acc_id: UUID | None = None
    from_acc_id: UUID | None = None
    start_date: date = date.today()
    end_date: date = date.today()
    amount: float = 100


@dataclass
class UpdateOrderAttribute(Command):
    id_: UUID
    attribute: str
    new_value: Any


@dataclass(frozen=True)
class CloseAccount(Command):
    id_: UUID
