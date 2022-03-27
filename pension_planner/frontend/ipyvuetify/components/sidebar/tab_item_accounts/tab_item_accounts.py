import logging
from uuid import UUID

from traitlets import traitlets
import ipyvuetify as v

from pension_planner import views
from pension_planner.domain import commands
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR
from pension_planner.service_layer.messagebus import MessageBus


class TabItemAccounts(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_accounts" / "tab_item_accounts_template.vue")

    tab = traitlets.Any().tag(sync=True)
    accounts = traitlets.Dict().tag(sync=True)

    def __init__(self, bus: MessageBus) -> None:
        self.bus = bus
        self.load_all_accounts()
        super().__init__()

    def load_all_accounts(self):
        accounts = views.fetch_all_accounts(self.bus.uow)
        self.accounts = {
            str(id_): {
                "name": name,
                "interest_rate": interest_rate,
            } for (id_, name, interest_rate) in accounts
        }

    def vue_open_account(self, _=None):
        command = commands.OpenAccount()
        self.bus.handle(command)

    def add_account(self, id_: UUID) -> None:
        account = views.fetch_account(id_, self.bus.uow)
        account.pop("id_")
        self.accounts = self.accounts | {str(id_): account}
        self.tab = len(self.accounts) - 1

    def vue_delete_account(self, id_: str):
        command = commands.CloseAccount(id_=UUID(id_))
        self.bus.handle(command)

    def delete_account(self, account_id: UUID):
        self.accounts = {id_: account
                         for id_, account in self.accounts.items()
                         if not id_ == str(account_id)}

    def vue_update_name(self, id_: str):
        command = commands.UpdateAccountAttribute(
            id_=UUID(id_),
            attribute="name",
            new_value=self.accounts[id_]["name"]
        )
        self.bus.handle(command)

    def vue_update_interest_rate(self, id_: str):
        value = float(self.accounts[id_]["interest_rate"]) / 100
        command = commands.UpdateAccountAttribute(
            id_=UUID(id_),
            attribute="interest_rate",
            new_value=value
        )
        self.bus.handle(command)
