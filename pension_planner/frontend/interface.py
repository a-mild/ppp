from abc import ABC, abstractmethod
from uuid import UUID

from pension_planner.domain import events
from pension_planner.service_layer.messagebus import MessageBus


class AbstractFrontendInterface(ABC):

    @abstractmethod
    def handle_account_opened(self, id_: UUID) -> None:
        ...

    @abstractmethod
    def handle_account_closed(self, id_: UUID) -> None:
        ...

    @abstractmethod
    def handle_order_created(self, id_: UUID) -> None:
        ...

    @abstractmethod
    def handle_order_deleted(self, id_: UUID) -> None:
        ...

    @abstractmethod
    def update_plotting_frontend(self, x: list[float], y: list[float]) -> None:
        ...

    @abstractmethod
    def handle_account_attribute_updated(self, event: events.AccountAttributeUpdated) -> None:
        ...

    @abstractmethod
    def handle_order_attribute_updated(self, event: events.OrderAttributeUpdated) -> None:
        ...

    @abstractmethod
    def setup(self, bus: MessageBus) -> None:
        ...
    