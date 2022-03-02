from typing import Any
from uuid import UUID

import ipyvuetify as v
import ipywidgets as w
import traitlets
from ipyvue import VueWidget
from traitlets import observe

from pension_planner import views
from pension_planner.domain import commands
from pension_planner.bootstrap import bus
from pension_planner.domain.commands import CreateSingleOrder, CreateStandingOrder, UpdateOrderAttribute
from pension_planner.domain.orders import ORDER_TYPES, ORDER_ATTRIBUTES
from pension_planner.frontend.components import COMPONENTS_DIR
from pension_planner.frontend.utils import obtain_widget
from pension_planner.service_layer.unit_of_work import AbstractUnitOfWork


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

    order_id = traitlets.Unicode().tag(sync=True)
    output = traitlets.Unicode().tag(sync=True)

    def __init__(self, *args, **kwargs):
        self.loading_new_order = None
        widgets = {parameter_name: obtain_widget(parameter_name)
                   for parameter_name in ORDER_ATTRIBUTES}
        # link widgets
        for parameter_name, widget in widgets.items():
            if isinstance(widget, VueWidget):
                names = "v_model"
            else:
                names = "value"
            widget.observe(lambda e: self.on_attribute_change(parameter_name, e))
        new_traits = {parameter_name: traitlets.Any(widget).tag(sync=True, **w.widget_serialization)
                      for parameter_name, widget in widgets.items()}
        self.add_traits(**new_traits)
        super().__init__(*args, **kwargs)

    def vue_place_order(self, name: str):
        if name == "SingleOrder":
            command = CreateSingleOrder()
        elif name == "StandingOrder":
            command = CreateStandingOrder()
        [id_] = bus.handle(command)
        self.order_id = str(id_)

    @observe("order_id")
    def on_order_id_changed(self, change, uow: AbstractUnitOfWork = bus.uow):
        self.loading_new_order = True
        new_id = UUID(change["new"])
        order = views.fetch_order(new_id, uow)
        self.output = f"{order!r}"
        self.update_dropdown_options(uow)
        for attribute, value in order.items():
            if attribute not in ORDER_ATTRIBUTES:
                continue
            widget = getattr(self, attribute)
            if isinstance(widget, VueWidget):
                setattr(widget, "v_model", value)
            else:
                setattr(widget, "value", value)
        self.loading_new_order = False

    def update_dropdown_options(self, uow: AbstractUnitOfWork = bus.uow):
        accounts = views.fetch_all_accounts(uow)
        options = [("Außenwelt", None)] + [(name, id_) for name, id_ in accounts.items()]
        self.from_acc_id.options = options
        self.target_acc_id.options = options

    def on_attribute_change(self, attribute: str, change: Any):
        if self.loading_new_order:
            return
        self.output = f"{attribute}\n{change!r}"
        command = UpdateOrderAttribute(
            id_=UUID(self.order_id),
            attribute=attribute,
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
