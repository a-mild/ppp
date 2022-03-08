from dataclasses import dataclass
from typing import Any
from uuid import UUID


class Event:
    pass


@dataclass(frozen=True)
class AccountOpened(Event):
    id_: UUID


@dataclass(frozen=True)
class AccountAttributeUpdated(Event):
    id_: UUID
    attribute: str
    old_value: Any
    new_value: Any


@dataclass(frozen=True)
class OrderCreated(Event):
    id_: UUID


@dataclass(frozen=True)
class OrderAttributeUpdated(Event):
    id_: UUID
    attribute: str
    old_value: Any
    new_value: Any
