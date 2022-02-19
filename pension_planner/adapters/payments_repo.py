from abc import ABC, abstractproperty, abstractmethod
from collections.abc import MutableMapping
from uuid import UUID

from pension_planner.domain.payments import PaymentBase, BalanceSheetSide

PaymentsMapping = MutableMapping[UUID, PaymentBase]


class AbstractPaymentsRepo(ABC):

    @property
    @abstractmethod
    def assets(self) -> list[PaymentBase]:
        return NotImplementedError

    @property
    @abstractmethod
    def liabilities(self) -> list[PaymentBase]:
        return NotImplementedError

    @abstractmethod
    def add_payment(self, payment: PaymentBase) -> None:
        return NotImplementedError

    @abstractmethod
    def add_payment(self, payment: PaymentBase) -> None:
        return NotImplementedError

    @abstractmethod
    def delete_payment(self, id_: UUID) -> None:
        return NotImplementedError


class InMemoryPaymentsRepo(AbstractPaymentsRepo):
    data: PaymentsMapping = {}

    def add_payment(self, payment: PaymentBase) -> None:
        self.data[payment.id_] = payment

    def get_payment(self, id_: UUID) -> PaymentBase:
        return self.data[id_]

    def delete_payment(self, id_: UUID) -> PaymentBase | None:
        return self.data.pop(id_, None)

    @property
    def assets(self) -> PaymentsMapping:
        return [p for p in self.data.values() if p.side == BalanceSheetSide.asset]

    @property
    def liabilities(self) -> PaymentsMapping:
        return [p for p in self.data.values() if p.side == BalanceSheetSide.liability]
