from dataclasses import dataclass
from uuid import UUID


class Event:
    pass


@dataclass(frozen=True)
class AccountOpened(Event):
    id_: UUID


@dataclass(frozen=True)
class OrderCreated(Event):
    id_: UUID
