import logging

import ipyvuetify as v
import ipywidgets as w
import traitlets

from pension_planner.domain.commands import OpenAccount
from pension_planner.frontend.components import COMPONENTS_DIR

from pension_planner.domain.orders import ORDER_TYPES
from pension_planner.service_layer.messagebus import handle
from pension_planner.service_layer.unit_of_work import InMemoryBankAccountRepositoryUnitOfWork


class AccountEditor(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "account_editor_template.vue")


class TabItemAccounts(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "tab_item_accounts_template.vue")

    account_name = traitlets.Unicode().tag(sync=True)
    interest_rate = traitlets.Float().tag(sync=True)
    # components = traitlets.Dict({
    #     "account-editor": AccountEditor
    # }).tag(sync=True, **v.VuetifyTemplate.class_component_serialization)

    def vue_open_account(self, data=None):
        command = OpenAccount()
        uow = InMemoryBankAccountRepositoryUnitOfWork()
        handle(command, uow)


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
