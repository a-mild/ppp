import logging
from uuid import UUID

from pension_planner import views
from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.frontend.ipyvuetify.components.app import App
from pension_planner.service_layer.messagebus import MessageBus


class IPyVuetifyFrontend(AbstractFrontendInterface):
    app = None

    @classmethod
    def handle_toggle_drawer(cls):
        cls.app.sidebar.toggle_drawer()

    @classmethod
    def handle_account_opened(cls, id_: UUID) -> None:
        assert cls.app is not None
        logging.debug("Called in ipyvuetify")
        cls.app.sidebar.tab_item_accounts.add_account(id_)

    @classmethod
    def setup(cls, bus: MessageBus) -> None:
        cls.app = App(bus)

    @classmethod
    def show(cls) -> App:
        return cls.app
