import logging
from uuid import UUID

import ipyvuetify as v
import traitlets

from pension_planner import views
from pension_planner.bootstrap import bus
from pension_planner.domain import commands
from pension_planner.domain.commands import OpenAccount
from pension_planner.frontend.components import COMPONENTS_DIR



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
    account_name = traitlets.Unicode().tag(sync=True)
    interest_rate = traitlets.Float().tag(sync=True)

    def vue_open_account(self, data=None):
        command = commands.OpenAccount()
        [id_] = bus.handle(command)
        acc = views.account_data(id_, bus.uow)
        self.accounts = self.accounts | {str(id_): acc}

    def vue_update_name(self, acc):
        self.output = f"Change name: {acc!r}"
        command = commands.UpdateAccountAttribute(
            id_=UUID(acc.id_),
            attribute="name",
            new_value=acc.get("name")
        )
        bus.handle(command)

    def vue_update_interest_rate(self, acc):
        self.output = f"Change interest: {acc!r}"
        command = commands.UpdateAccountAttribute(
                    id_=UUID(acc.id_),
                    attribute="interest_rate",
                    new_value=acc.get("interest_rate")
                )
        bus.handle(command)


class TabItemOrders(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "tab_item_orders_template.vue")


class SideBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar_template.vue")

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)
    components = traitlets.Dict({
        "tab-item-accounts": TabItemAccounts,
        "tab-item-orders": TabItemOrders,
    }).tag(sync=True, **v.VuetifyTemplate.class_component_serialization)

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open
