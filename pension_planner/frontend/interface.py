from abc import ABC, abstractmethod
from uuid import UUID


class AbstractFrontendInterface(ABC):

    @abstractmethod
    def handle_account_opened(self, id_: UUID) -> None:
        ...

    @abstractmethod
    def handle_account_closed(self, id_: UUID) -> None:
        ...
    