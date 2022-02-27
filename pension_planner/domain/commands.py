from dataclasses import dataclass

from pension_planner.domain.orders import OrderBase


class Event:
    pass


@dataclass
class ToggleDrawer(Event):
    pass

@dataclass
class SelectBankAccount(Event):
    pass


@dataclass
class BankAccountCreated(Event):
    name: str | None = None
    orders: list[OrderBase] | None = None
    interest_rate: float | None = None


