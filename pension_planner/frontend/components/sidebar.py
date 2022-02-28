import logging
from dataclasses import asdict

import ipyvuetify as v
import traitlets

from pension_planner.adapters import orm
from pension_planner.domain.commands import OpenAccount
from pension_planner.frontend.components import COMPONENTS_DIR

from pension_planner.service_layer.messagebus import handle
from pension_planner.service_layer.unit_of_work import SQLAlchemyAccountsUnitOfWork


orm.start_mappers()


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
    # components = traitlets.Dict({
    #     "account-editor": AccountEditor
    # }).tag(sync=True, **v.VuetifyTemplate.class_component_serialization)
    output = traitlets.Any().tag(sync=True)

    def vue_open_account(self, data=None):
        self.output = f"Open account"
        command = OpenAccount()
        uow = SQLAlchemyAccountsUnitOfWork()
        [account] = handle(command, uow)
        self.output = f"{account!r}"
        self.accounts = self.accounts | {account.id_: asdict(account)}
        self.output = f"{self.accounts!r}"

    def vue_update_name(self, acc):
        self.output = f"Change name: {acc!r}"

    def vue_update_interest_rate(self, acc):
        self.output = f"Change interest: {acc!r}"


class TabItemOrders(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "tab_item_orders_template.vue")


class SideBar(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar_template.vue")
    #order_types = traitlets.List(default_value=list(ORDER_TYPES.keys())).tag(sync=True)

    drawer_open = traitlets.Bool(default_value=False).tag(sync=True)
    components = traitlets.Dict({
        "tab-item-accounts": TabItemAccounts,
        "tab-item-orders": TabItemOrders,
    }).tag(sync=True, **v.VuetifyTemplate.class_component_serialization)

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open
