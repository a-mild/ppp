import logging
import random
from uuid import UUID

from pension_planner import views
from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.frontend.ipyvuetify.components.app import App
from pension_planner.plotting_frontend.interface import AbstractPlottingFrontend
from pension_planner.plotting_frontend.plotly import PlotlyPlottingFrontend
from pension_planner.service_layer.messagebus import MessageBus


class IPyVuetifyFrontend(AbstractFrontendInterface):

    app: App | None = None
    plotting_frontend: AbstractPlottingFrontend | None = None

    @classmethod
    def handle_toggle_drawer(cls):
        cls.app.sidebar.toggle_drawer()

    @classmethod
    def handle_account_opened(cls, id_: UUID) -> None:
        assert cls.app is not None
        cls.app.sidebar.tab_item_accounts.add_account(id_)

    @classmethod
    def handle_account_closed(cls, id_: UUID) -> None:
        cls.app.sidebar.tab_item_accounts.delete_account(id_)

    @classmethod
    def handle_order_created(cls, id_: UUID) -> None:
        cls.app.sidebar.tab_item_orders.order_editor.add_order(id_)

    @classmethod
    def handle_order_deleted(cls, id_: UUID) -> None:
        cls.app.sidebar.tab_item_orders.order_editor.delete_order(id_)

    @classmethod
    def update_plotting_frontend(cls, x: list[float] = None, y: list[float] = None) -> None:
        x = list(range(10))
        y = [random.randint(0, 10) for _ in range(10)]
        cls.plotting_frontend.update_with(x, y)

    @classmethod
    def setup(cls, bus: MessageBus) -> None:
        cls.app = App(bus)
        cls.plotting_frontend = PlotlyPlottingFrontend(cls.app.main)

    @classmethod
    def show(cls) -> App:
        return cls.app
