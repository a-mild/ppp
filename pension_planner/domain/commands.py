from dataclasses import dataclass, field

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
    name: str = field(default_factory=next(name_factory))
    orders: list[OrderBase] = field(default_factory=list)
    interest_rate: float = 0.0
