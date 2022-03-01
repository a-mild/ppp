import logging
from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
import traitlets

from pension_planner import views
from pension_planner.bootstrap import bus
from pension_planner.domain import commands
from pension_planner.domain.commands import CreateSingleOrder, CreateStandingOrder, UpdateOrderAttribute
from pension_planner.domain.orders import ORDER_TYPES, SingleOrder, StandingOrder
from pension_planner.frontend.components import COMPONENTS_DIR


ORDER_ATTRIBUTES = SingleOrder.__dataclass_fields__.keys() | StandingOrder.__dataclass_fields__.keys()

class AccountEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "account_editor_template.vue")


ACCOUNT_DATA = {
    "1": {"id_": 1,
          "name": "Bankkonto #1",
          "interest_rate": 1.0},
    "2": {"id_": 2,
          "name": "Bankkonto #2",
          "interest_rate": 2.0},
}


class TabItemAccounts(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "tab_item_accounts_template.vue")

    tab = traitlets.Any().tag(sync=True)

    accounts = traitlets.Dict().tag(sync=True)

    def vue_open_account(self, data=None):
        command = commands.OpenAccount()
        [id_] = bus.handle(command)
        acc = views.fetch_account(id_, bus.uow)
        self.accounts = self.accounts | {str(id_): acc}

    def vue_update_name(self, acc):
        command = commands.UpdateAccountAttribute(
            id_=UUID(acc.id_),
            attribute="name",
            new_value=acc.get("name")
        )
        bus.handle(command)

    def vue_update_interest_rate(self, acc):
        command = commands.UpdateAccountAttribute(
            id_=UUID(acc.id_),
            attribute="interest_rate",
            new_value=acc.get("interest_rate")
        )
        bus.handle(command)


class TabItemOrders(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "tab_item_orders_template.vue")

    order_names = traitlets.List(default_value=list(ORDER_TYPES.keys())).tag(sync=True)

    control_widgets = traitlets.List().tag(sync=True, **w.widget_serialization)

    selected_id = traitlets.Unicode()
    output = traitlets.Unicode().tag(sync=True)

    def vue_place_order(self, name: str):
        if name == "SingleOrder":
            command = CreateSingleOrder()
        elif name == "StandingOrder":
            command = CreateStandingOrder()
        [id_] = bus.handle(command)

    def on_name_change(self, change=None):
        command = UpdateOrderAttribute(
            id_=UUID(self.selected_id),
            attribute="name",
            new_value=change["new"])
        bus.handle(command)


class SideBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar_template.vue")

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)

    tab_item_accounts = traitlets.Any().tag(sync=True, **w.widget_serialization)
    tab_item_orders = traitlets.Any().tag(sync=True, **w.widget_serialization)

    def __init__(self, *args, **kwargs):
        self.tab_item_accounts = TabItemAccounts()
        self.tab_item_orders = TabItemOrders()
        super().__init__(*args, **kwargs)

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open
