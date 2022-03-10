from uuid import UUID

from traitlets import traitlets
import ipyvuetify as v

from pension_planner import views
from pension_planner.bootstrap import bus
from pension_planner.domain import commands
from pension_planner.frontend.ipyvuetify.components import COMPONENTS_DIR


class TabItemAccounts(v.VuetifyTemplate):
    template_file = str(COMPONENTS_DIR / "sidebar" / "tab_item_accounts" / "tab_item_accounts_template.vue")

    tab = traitlets.Any().tag(sync=True)

    accounts = traitlets.Dict().tag(sync=True)

    def vue_open_account(self, data=None):
        command = commands.OpenAccount()
        [id_] = bus.handle(command)
        acc = views.fetch_account(id_, bus.uow)
        acc.pop("id_")
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
