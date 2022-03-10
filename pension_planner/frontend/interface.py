from abc import ABC, abstractmethod


class AbstractFrontendInterface(ABC):

    @abstractmethod
    def handle_account_opened(self):
        ...