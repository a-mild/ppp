import logging
from uuid import UUID

import pandas as pd

from pension_planner.domain import events
from pension_planner.frontend.interface import AbstractFrontendInterface
from pension_planner.frontend.ipyvuetify.components.app import App
from pension_planner.plotting_frontend.interface import AbstractPlottingFrontend
from pension_planner.plotting_frontend.plotly import PlotlyPlottingFrontend
from pension_planner.service_layer.messagebus import MessageBus


class IPyVuetifyFrontend(AbstractFrontendInterface):

    def __init__(self):
        self.app = None
        self.plotting_frontend = None

    def handle_toggle_drawer(self):
        self.app.sidebar.toggle_drawer()
        self.app.footer.output = "Toggled Drawer"

    def handle_account_opened(self, id_: UUID) -> None:
        assert self.app is not None
        self.app.sidebar.tab_item_accounts.add_account(id_)
        self.app.sidebar.tab_item_orders.order_editor.update_dropdowns()
        self.app.footer.output = "Opened Account"

    def handle_account_closed(self, id_: UUID) -> None:
        self.app.sidebar.tab_item_accounts.delete_account(id_)
        # self.app.sidebar.tab_item_orders.order_editor.update_dropdowns()

    def handle_account_attribute_updated(self, event: events.AccountAttributeUpdated) -> None:
        if event.attribute == "name":
            self.app.sidebar.tab_item_orders.order_editor.update_dropdowns()

    def handle_order_created(self, id_: UUID) -> None:
        self.app.sidebar.tab_item_orders.order_editor.add_order(id_)

    def handle_order_deleted(self, id_: UUID) -> None:
        self.app.sidebar.tab_item_orders.order_editor.delete_order(id_)

    def handle_order_attribute_updated(self, event: events.OrderAttributeUpdated) -> None:
        pass

    def update_plotting_frontend(self, df: pd.DataFrame) -> None:
        self.plotting_frontend.update_with(df)
        self.app.footer.output = f"Updated plot :)"

    def setup(self, bus: MessageBus) -> None:
        self.app = App(bus)
        self.plotting_frontend = PlotlyPlottingFrontend(self.app.main)

    def show(self) -> App:
        return self.app
